import folium
import numpy as np
from PIL import Image
import io
import os


def create_map_with_lines(lines_data, output_path):
    """
    创建地图并绘制多条线，自动调整缩放级别以显示所有线段

    参数：
    lines_data: 列表的列表，每个子列表包含一条线的坐标点 [[(lat1, lon1), (lat2, lon2), ...], [...]]
    output_path: 输出PNG文件的路径
    """

    # 计算所有坐标的边界
    all_lats = []
    all_lons = []
    for line in lines_data:
        lats, lons = zip(*line)
        all_lats.extend(lats)
        all_lons.extend(lons)

    # 计算中心点
    center = [np.mean(all_lats), np.mean(all_lons)]

    # 计算边界框
    bounds = [
        [min(all_lats), min(all_lons)],  # 西南角
        [max(all_lats), max(all_lons)]  # 东北角
    ]

    # 创建地图
    m = folium.Map(
        location=center,
        zoom_start=12,  # 初始缩放级别，会被fit_bounds覆盖
        tiles=None
    )

    # 添加天地图作为底图
    tianditu_url = (
        "http://t7.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=baef27b004fae0eca6b5187854d3f1af")

    folium.TileLayer(
        tiles=tianditu_url,
        attr='天地图',
        name='天地图影像图'
    ).add_to(m)

    # 为每条线随机生成不同的颜色
    colors = [f'#{np.random.randint(0, 16777215):06x}' for _ in range(len(lines_data))]

    # 绘制每条线
    for line, color in zip(lines_data, colors):
        folium.PolyLine(
            locations=line,
            weight=2,
            color=color,
            opacity=0.8
        ).add_to(m)

    # 调整地图视图以适应所有线段
    m.fit_bounds(bounds)

    # 保存为HTML
    temp_html = 'temp_map.html'
    m.save(temp_html)

    # 将HTML转换为PNG
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(f'file://{os.path.abspath(temp_html)}')

        # 等待地图加载完成
        import time
        time.sleep(10)

        # 截图并保存
        driver.save_screenshot(output_path)
        driver.quit()
    finally:
        pass
        # if os.path.exists(temp_html):
        #     os.remove(temp_html)


# 使用示例
if __name__ == "__main__":
    # 示例数据
    lines_data = [
        [(31.175458920, 121.274351550), (31.175879180, 121.274145440), (31.175925200, 121.274120570)]
    ]

    output_path = "output_map.png"
    create_map_with_lines(lines_data, output_path)