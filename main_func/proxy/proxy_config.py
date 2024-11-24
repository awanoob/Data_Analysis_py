import os
import json
import logging
import urllib3
import certifi
import winreg
from typing import Dict, Optional, List
from urllib.parse import urlparse
from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkProxy


class ProxyManager:
    """代理管理类"""
    _instance = None

    def __new__(cls):
        # 单例模式
        if cls._instance is None:
            cls._instance = super(ProxyManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.proxy_settings = self._load_proxy_settings()
            if self.proxy_settings:
                self._setup_proxy()  # 只有代理存在时才配置
            else:
                logging.info("未加载到代理设置，程序将在无代理模式下运行")
            self.initialized = True

    def _get_windows_proxy_settings(self) -> Optional[Dict[str, str]]:
        """从Windows注册表获取代理设置"""
        try:
            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, winreg.KEY_READ
            )

            # 检查代理是否启用
            proxy_enable, _ = winreg.QueryValueEx(reg_key, "ProxyEnable")
            if not proxy_enable:
                winreg.CloseKey(reg_key)
                return None

            # 获取代理服务器地址
            proxy_server, _ = winreg.QueryValueEx(reg_key, "ProxyServer")

            # 获取不使用代理的地址列表
            try:
                proxy_override, _ = winreg.QueryValueEx(reg_key, "ProxyOverride")
                bypass_list = proxy_override.split(";")
            except WindowsError:
                bypass_list = []

            winreg.CloseKey(reg_key)

            # 解析代理服务器地址
            settings = {}
            if "=" in proxy_server:  # 分别设置了http和https代理
                for part in proxy_server.split(";"):
                    if "=" in part:
                        protocol, url = part.split("=", 1)
                        settings[protocol] = url
            else:  # 统一的代理地址
                settings["http"] = proxy_server
                settings["https"] = proxy_server

            settings["bypass"] = bypass_list
            logging.info("从Windows系统加载代理设置成功")
            return settings

        except WindowsError as e:
            logging.error(f"读取Windows代理设置失败: {str(e)}")
            return None

    def _load_proxy_settings(self) -> Optional[Dict[str, str]]:
        """加载代理设置"""
        # 首先尝试从Windows系统获取
        settings = self._get_windows_proxy_settings()
        if settings:
            return settings

        try:
            # 尝试从配置文件读取
            with open('proxy_config.json', 'r') as f:
                settings = json.load(f)
                logging.info("从配置文件加载代理设置成功")
                return settings
        except FileNotFoundError:
            # 尝试从环境变量读取
            http_proxy = os.environ.get('http_proxy')
            https_proxy = os.environ.get('HTTPS_PROXY')
            if http_proxy or https_proxy:
                settings = {}
                if http_proxy:
                    settings['http'] = http_proxy
                if https_proxy:
                    settings['https'] = https_proxy
                logging.info("从环境变量加载代理设置成功")
                return settings
            logging.info("未找到代理设置")
            return None
        except Exception as e:
            logging.error(f"加载代理设置时出错: {str(e)}")
            return None

    def _setup_proxy(self):
        """设置全局代理"""
        if not self.proxy_settings:  # 代理设置为空，清除环境变量
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)
            os.environ.pop('NO_PROXY', None)
            logging.info("未检测到代理设置，已清除代理环境变量")
            return
        try:
            # 设置环境变量
            if 'https' in self.proxy_settings:
                os.environ['HTTPS_PROXY'] = self.proxy_settings['https']
                os.environ['HTTP_PROXY'] = self.proxy_settings.get('http', self.proxy_settings['https'])
            elif 'http' in self.proxy_settings:
                os.environ['HTTP_PROXY'] = self.proxy_settings['http']

            # 设置Qt代理
            if 'https' in self.proxy_settings or 'http' in self.proxy_settings:
                self._setup_qt_proxy()

            # 设置bypass列表
            if 'bypass' in self.proxy_settings:
                os.environ['NO_PROXY'] = ','.join(self.proxy_settings['bypass'])

            logging.info("代理设置已应用")
        except Exception as e:
            logging.error(f"设置代理时出错: {str(e)}")

    def _setup_qt_proxy(self):
        """设置Qt应用的代理"""
        try:
            proxy_url = self.get_proxy_url()
            if not proxy_url:  # 无代理，跳过配置
                logging.info("未检测到Qt代理URL，跳过Qt代理配置")
                return

            url = QUrl(proxy_url)
            proxy = QNetworkProxy()
            proxy.setType(QNetworkProxy.ProxyType.HttpProxy)
            proxy.setHostName(url.host())
            if url.port() != -1:
                proxy.setPort(url.port())

            # 设置不使用代理的地址
            if 'bypass' in self.proxy_settings:
                proxy.setHostName(','.join(self.proxy_settings['bypass']))

            QNetworkProxy.setApplicationProxy(proxy)
            logging.info("Qt代理设置成功")
        except Exception as e:
            logging.error(f"设置Qt代理时出错: {str(e)}")

    def get_proxy_url(self) -> Optional[str]:
        """获取代理URL"""
        if not self.proxy_settings:
            return None
        return self.proxy_settings.get('https', self.proxy_settings.get('http'))

    def get_urllib3_pool(self, server_hostname: Optional[str] = None) -> urllib3.PoolManager:
        """获取配置好代理的urllib3连接池"""
        try:
            if self.proxy_settings:
                proxy_url = self.get_proxy_url()
                if proxy_url:
                    return urllib3.ProxyManager(
                        proxy_url,
                        cert_reqs='CERT_REQUIRED',
                        ca_certs=certifi.where(),
                        server_hostname=server_hostname
                    )
            # 如果没有代理设置，返回默认连接池
            return urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
        except Exception as e:
            logging.error(f"获取urllib3连接池时出错: {str(e)}")
            return urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )

    def get_chrome_options(self) -> Dict:
        """获取Chrome代理设置"""
        options = {
            "chrome_options": [
                "--headless",
                "--window-size=1920x1080",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        }

        if self.proxy_settings:
            proxy_url = self.get_proxy_url()
            if proxy_url:
                options["chrome_options"].append(f"--proxy-server={proxy_url}")
                options["ssl_verify"] = False  # 禁用SSL验证以避免代理问题

        return options

    @property
    def has_proxy(self) -> bool:
        """检查是否配置了代理"""
        return bool(self.proxy_settings)
