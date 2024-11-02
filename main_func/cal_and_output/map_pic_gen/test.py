import winreg
import urllib.request
import os
import socket
import requests


def get_windows_proxy_settings():
    """获取Windows系统的代理设置"""
    proxy_settings = {}

    try:
        # 打开注册表键
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_READ
        )

        # 获取代理是否启用
        proxy_enable, _ = winreg.QueryValueEx(reg_key, "ProxyEnable")
        proxy_settings["enabled"] = bool(proxy_enable)

        # 获取代理服务器地址
        if proxy_enable:
            proxy_server, _ = winreg.QueryValueEx(reg_key, "ProxyServer")
            proxy_settings["server"] = proxy_server

        # 获取bypass列表
        try:
            proxy_override, _ = winreg.QueryValueEx(reg_key, "ProxyOverride")
            proxy_settings["bypass"] = proxy_override.split(";")
        except WindowsError:
            proxy_settings["bypass"] = []

        winreg.CloseKey(reg_key)
    except WindowsError:
        return {"error": "无法读取注册表"}

    return proxy_settings


def get_environment_proxies():
    """获取环境变量中的代理设置"""
    return {
        "http_proxy": os.environ.get("http_proxy", ""),
        "https_proxy": os.environ.get("https_proxy", ""),
        "no_proxy": os.environ.get("no_proxy", "")
    }


def check_proxy_connection(proxy):
    """测试代理连接"""
    try:
        proxies = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    # 获取Windows代理设置
    print("Windows代理设置:")
    windows_settings = get_windows_proxy_settings()
    for key, value in windows_settings.items():
        print(f"{key}: {value}")

    print("\n环境变量代理设置:")
    env_proxies = get_environment_proxies()
    for key, value in env_proxies.items():
        print(f"{key}: {value}")

    # 如果代理已启用，测试连接
    if windows_settings.get("enabled") and windows_settings.get("server"):
        print(f"\n测试代理连接 ({windows_settings['server']})...")
        connection_ok = check_proxy_connection(windows_settings["server"])
        print(f"代理连接测试: {'成功' if connection_ok else '失败'}")


if __name__ == "__main__":
    main()