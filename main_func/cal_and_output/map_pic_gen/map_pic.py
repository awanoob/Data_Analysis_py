import folium
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import logging
from typing import List, Tuple, Union
import tempfile
from main_func.proxy.proxy_config import ProxyManager


class MapGenerator:
    def __init__(self):
        self.colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        self.api_key = "baef27b004fae0eca6b5187854d3f1af"
        self.proxy_manager = ProxyManager()
        self._driver = None

    def _create_chrome_driver(self):
        """创建Chrome WebDriver，支持代理设置"""
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--ignore-certificate-errors')

            # 修改代理部分的判断逻辑
            try:
                if self.proxy_manager.has_proxy:
                    proxy_url = self.proxy_manager.get_proxy_url()
                    if proxy_url:
                        logging.info(f"使用代理：{proxy_url}")
                        options.add_argument(f'--proxy-server={proxy_url}')
                        if 'bypass' in self.proxy_manager.proxy_settings:
                            bypass_list = ','.join(self.proxy_manager.proxy_settings['bypass'])
                            options.add_argument(f'--proxy-bypass-list={bypass_list}')
            except Exception as proxy_error:
                logging.warning(f"代理设置失败，将不使用代理: {str(proxy_error)}")

            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self._driver.set_page_load_timeout(30)
            self._driver.set_script_timeout(30)
            return self._driver

        except Exception as e:
            logging.error(f"创建Chrome WebDriver失败: {str(e)}")
            raise

    def _cleanup_driver(self):
        """清理WebDriver资源"""
        try:
            if self._driver:
                self._driver.quit()
                self._driver = None
        except Exception as e:
            logging.warning(f"清理WebDriver时出错: {str(e)}")

    def _create_map(self, center: List[float], zoom: int) -> folium.Map:
        """创建基础地图"""
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles=None,
            crs = 'EPSG4326'
        )

        # 使用img_c（影像底图，经纬度投影）
        img_url = (
            "http://t7.tianditu.gov.cn/img_c/wmts?"
            "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&"
            "LAYER=img&STYLE=default&TILEMATRIXSET=c&FORMAT=tiles&"
            f"TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&tk={self.api_key}"
        )

        folium.TileLayer(
            tiles=img_url,
            attr='天地图',
            name='天地图影像图',
            zoomOffset = 1
        ).add_to(m)

        # # 添加标注图层（cia_c是经纬度投影的标注）
        # anno_url = (
        #     "http://t{s}.tianditu.gov.cn/cia_c/wmts?"
        #     "SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&"
        #     "LAYER=cia&STYLE=default&TILEMATRIXSET=c&FORMAT=tiles&"
        #     f"TILEMATRIX={{z}}&TILEROW={{y}}&TILECOL={{x}}&tk={self.api_key}"
        # )
        #
        # folium.TileLayer(
        #     tiles=anno_url,
        #     attr='天地图标注',
        #     name='天地图标注',
        #     overlay=True
        # ).add_to(m)

        return m

    def _add_lines_to_map(self, map_obj: folium.Map, lines_data: List[List[Tuple[float, float]]]):
        """向地图添加多条线"""
        for i, line in enumerate(lines_data):
            color = self.colors[i % len(self.colors)]
            # 不需要转换坐标，直接使用经纬度
            folium.PolyLine(
                locations=line,
                weight=2,
                color=color,
                opacity=0.8,
                popup=f'轨迹 {i + 1}'
            ).add_to(map_obj)

        if len(lines_data) > 1:
            legend_html = """
                <div style="position: fixed; 
                            bottom: 50px; right: 50px; width: 120px;
                            border:2px solid grey; z-index:9999; 
                            background-color:white;
                            padding: 10px;
                            font-size: 14px;">
                    <p><strong>图例</strong></p>
            """
            for i in range(len(lines_data)):
                color = self.colors[i % len(self.colors)]
                legend_html += f"""
                    <p>
                        <span style="background-color: {color};
                                    width: 15px;
                                    height: 15px;
                                    display: inline-block;
                                    margin-right: 5px;"></span>
                        轨迹 {i + 1}
                    </p>
                """
            legend_html += "</div>"
            map_obj.get_root().html.add_child(folium.Element(legend_html))

    def _save_map_screenshot(self, map_obj: folium.Map, output_path: str):
        """保存地图截图，包含错误处理和资源清理"""
        temp_html = None
        try:
            # 创建临时文件
            fd, temp_html = tempfile.mkstemp(suffix='.html')
            os.close(fd)  # 立即关闭文件描述符

            # 保存地图到临时HTML文件
            map_obj.save(temp_html)

            # 创建driver并获取截图
            driver = self._create_chrome_driver()
            driver.get(f'file://{os.path.abspath(temp_html)}')
            time.sleep(3)  # 等待地图加载
            driver.save_screenshot(output_path)

        except Exception as e:
            logging.error(f"保存地图截图失败: {str(e)}")
            raise
        finally:
            # 清理资源
            self._cleanup_driver()
            # 删除临时文件
            if temp_html and os.path.exists(temp_html):
                try:
                    os.unlink(temp_html)
                except Exception as e:
                    logging.warning(f"删除临时文件失败: {str(e)}")

    def _calculate_zoom_level(self, bounds: List[List[float]]) -> int:
        """
        根据边界范围计算合适的缩放级别
        bounds: [[min_lat, min_lon], [max_lat, max_lon]]
        """
        lat_diff = bounds[1][0] - bounds[0][0]  # 纬度差
        lon_diff = bounds[1][1] - bounds[0][1]  # 经度差

        # 计算最大跨度（度）
        max_diff = max(lat_diff, lon_diff)

        # 缩放级别映射表（近似值）：
        # 跨度 -> 缩放级别
        zoom_mapping = {
            0.0001: 20,  # ~10m
            0.001: 17,  # ~100m
            0.01: 14,  # ~1km
            0.1: 11,  # ~10km
            1: 8,  # ~100km
            10: 5,  # ~1000km
        }

        # 找到最接近的缩放级别
        for span, zoom in sorted(zoom_mapping.items()):
            if max_diff <= span:
                return zoom

        return 4  # 默认最小缩放级别

    def create_maps(self, lines_data: List[List[Tuple[float, float]]],
                    output_path_full: str, output_path_zoomed: str):
        """创建地图（全局视图和局部视图）"""
        try:
            # 计算所有点的边界
            all_coords = [(lat, lon) for line in lines_data for lat, lon in line]
            all_lats, all_lons = zip(*all_coords)

            center = [np.mean(all_lats), np.mean(all_lons)]
            bounds = [[min(all_lats), min(all_lons)], [max(all_lats), max(all_lons)]]

            # 为全局视图计算合适的缩放级别
            full_zoom = self._calculate_zoom_level(bounds)

            # 为局部视图选择一个随机点
            random_point = all_coords[np.random.randint(0, len(all_coords))]

            # 创建两个地图
            for is_zoomed, output_path in [(False, output_path_full), (True, output_path_zoomed)]:
                m = self._create_map(
                    random_point if is_zoomed else center,
                    17 if is_zoomed else full_zoom  # 使用计算得到的缩放级别
                )
                self._add_lines_to_map(m, lines_data)
                if not is_zoomed:
                    m.fit_bounds(bounds)

                self._save_map_screenshot(m, output_path)

        except Exception as e:
            logging.error(f"生成地图失败: {str(e)}")
            raise


def map_generator(datapaths: Union[str, List[str]], output_path_full, output_path_zoomed) -> None:
    """生成地图的主函数"""
    try:
        if isinstance(datapaths, str):
            datapaths = [datapaths]

        lines_data = []
        for datapath in datapaths:
            try:
                data = pd.read_csv(datapath, sep=" ", header=None)
                if not data.empty:
                    line_coords = [(row[3], row[4]) for row in data.itertuples()]
                    lines_data.append(line_coords)
            except Exception as e:
                logging.warning(f"读取文件 {datapath} 失败: {str(e)}")
                continue

        if not lines_data:
            raise ValueError("没有成功读取任何轨迹数据")

        map_generate = MapGenerator()
        map_generate.create_maps(
            lines_data,
            output_path_full,
            output_path_zoomed
        )

    except Exception as e:
        logging.error(f"地图生成失败: {str(e)}")
        raise
