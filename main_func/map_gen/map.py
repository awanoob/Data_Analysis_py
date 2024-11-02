import folium
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


def create_map_with_lines_and_zoom(lines_data, output_path_full, output_path_zoomed):
    """
    创建两张地图：
    1. 第一张地图绘制多条线并自动调整缩放级别以显示所有线段。
    2. 第二张地图缩放到最大级别并聚焦到所有点的中心或随机选择一个点。

    参数：
    lines_data: 列表的列表，每个子列表包含一条线的坐标点 [[(lat1, lon1), (lat2, lon2), ...], [...]]
    output_path_full: 自动调整缩放的地图输出路径
    output_path_zoomed: 缩放到最大级别的地图输出路径
    """

    # 计算所有坐标的边界
    all_lats, all_lons = [], []
    for line in lines_data:
        lats, lons = zip(*line)
        all_lats.extend(lats)
        all_lons.extend(lons)

    # 计算地图中心和边界框
    center = [np.mean(all_lats), np.mean(all_lons)]
    bounds = [[min(all_lats), min(all_lons)], [max(all_lats), max(all_lons)]]

    # 随机选择一个点用于最大缩放
    random_index = np.random.randint(0, len(all_lats))
    random_point = [all_lats[random_index], all_lons[random_index]]

    # 创建地图函数
    def create_and_save_map(m, file_name, zoom_bounds=None):
        # 绘制线段
        for line in lines_data:
            folium.PolyLine(locations=line, weight=2, color='blue', opacity=0.8).add_to(m)
        # 调整地图视图
        if zoom_bounds:
            m.fit_bounds(zoom_bounds)
        m.save(file_name)

        # 使用Selenium加载HTML并截图
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(f'file://{os.path.abspath(file_name)}')

        # 等待地图加载完成
        time.sleep(5)

        # 截图并保存
        driver.save_screenshot(file_name.replace('.html', '.png'))
        driver.quit()

        # 删除临时HTML文件
        # if os.path.exists(file_name):
        #     os.remove(file_name)

    # 第一张图：自动调整缩放
    m_full = folium.Map(location=center, zoom_start=12, tiles=None)
    tianditu_url = ("http://t7.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile"
                    "&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles"
                    "&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=baef27b004fae0eca6b5187854d3f1af")
    folium.TileLayer(tiles=tianditu_url, attr='天地图', name='天地图影像图').add_to(m_full)

    create_and_save_map(m_full, 'temp_map_full.html', zoom_bounds=bounds)

    # 检查文件是否存在并删除旧文件
    if os.path.exists(output_path_full):
        os.remove(output_path_full)
    os.rename('temp_map_full.png', output_path_full)

    # 第二张图：缩放到最大，并聚焦到随机选择的点
    m_zoomed = folium.Map(location=random_point, zoom_start=18, tiles=None)  # 缩放到最大
    folium.TileLayer(tiles=tianditu_url, attr='天地图', name='天地图影像图').add_to(m_zoomed)

    create_and_save_map(m_zoomed, 'temp_map_zoomed.html')

    # 检查文件是否存在并删除旧文件
    if os.path.exists(output_path_zoomed):
        os.remove(output_path_zoomed)
    os.rename('temp_map_zoomed.png', output_path_zoomed)


if __name__ == "__main__":
    # 读取数据
    data = pd.read_csv("220prodec_rtkplot.txt", sep=" ", header=None)
    lines_data = [(data.iloc[i, 2], data.iloc[i, 3]) for i in range(len(data))]
    lines_data = [lines_data]
    output_path_full = "output_map_full.png"
    output_path_zoomed = "output_map_zoomed.png"
    create_map_with_lines_and_zoom(lines_data, output_path_full, output_path_zoomed)
