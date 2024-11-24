import numpy as np
from pyproj import Proj, Transformer
from copy import deepcopy


def wgs84_to_enu(lat: np.ndarray, lon: np.ndarray, alt: np.ndarray, ref_lat: np.ndarray, ref_lon: np.ndarray, ref_alt: np.ndarray) -> np.ndarray:
    # 将WGS84坐标转为ECEF坐标
    ref_proj_str = "+proj=geocent +datum=WGS84"
    transformer = Transformer.from_crs("EPSG:4326", ref_proj_str)
    x, y, z = transformer.transform(lat, lon, alt)
    ref_x, ref_y, ref_z = transformer.transform(ref_lat, ref_lon, ref_alt)
    dx = x - ref_x
    dy = y - ref_y
    dz = z - ref_z
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)
    e = -np.sin(lon_rad) * dx + np.cos(lon_rad) * dy
    n = -np.sin(lat_rad) * np.cos(lon_rad) * dx - np.sin(lat_rad) * np.sin(lon_rad) * dy + np.cos(lat_rad) * dz
    u = np.cos(lat_rad) * np.cos(lon_rad) * dx + np.cos(lat_rad) * np.sin(lon_rad) * dy + np.sin(lat_rad) * dz
    return e, n, u


def wgs84_to_utm(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    # 根据经度自动选择合适的UTM坐标系
    utm_zone = np.floor((lon + 180) / 6).astype(int) + 1
    unique_zones = np.unique(utm_zone)

    easting = np.zeros_like(lat)
    northing = np.zeros_like(lon)

    for zone in unique_zones:
        mask = utm_zone == zone
        utm_proj_str = f"+proj=utm +zone={zone} +datum=WGS84"
        transformer = Transformer.from_crs("EPSG:4326", utm_proj_str)
        easting[mask], northing[mask] = transformer.transform(lat[mask], lon[mask])

    return easting, northing


def get_distance(e: np.ndarray, n: np.ndarray, alt: np.ndarray, ve: np.ndarray, vn: np.ndarray) -> np.ndarray:
    distance = np.zeros_like(e)
    dis_diff = 0
    v0 = np.sqrt(np.power(ve, 2) + np.power(vn, 2))
    for i in range(len(e)):
        if v0[i] > 0.02:
            dis_diff += np.sqrt(np.power(e[i] - e[i-1], 2) + np.power(n[i] - n[i-1], 2) + np.power(alt[i] - alt[i-1], 2))
            distance[i] = dis_diff[0]
        else:
            distance[i] = distance[i - 1]
    return distance


def check_deg(deg_input: np.ndarray) -> np.ndarray:
    deg_output = np.zeros((len(deg_input), 1))
    for i in range(len(deg_input)):
        if deg_input[i] > 180:
            deg_output[i] = deg_input[i] - 360
        elif deg_input[i] < -180:
            deg_output[i] = deg_input[i] + 360
        else:
            deg_output[i] = deg_input[i]
    return deg_output


def syserr_cal_alg(data: np.ndarray) -> float:
    data = data.copy()  # 避免修改原始数据
    for _ in range(5):
        mean_val = np.mean(data)
        deviations = np.abs(data - mean_val)  # 计算绝对偏差
        sorted_devs = np.sort(deviations)    # 排序绝对偏差

        if sorted_devs.size > 0:
            # 计算 2.5 倍中值绝对偏差的阈值
            sigma = sorted_devs[int(len(sorted_devs) / 2)] / 0.6745 * 2.5
        else:
            sigma = 0

        # 生成布尔掩码，过滤掉偏差超过阈值的元素
        mask = deviations <= sigma
        data = data[mask]  # 应用掩码，保留符合条件的数据
    return np.mean(data)


def get_syserr(x, y, alt, roll, pitch, heading, input_cfg, postype) -> dict:
    syserr = {"x": 0, "y": 0, "alt": 0, "roll": 0, "pitch": 0, "heading": 0}
    fix_ratio = np.count_nonzero(postype == 1) / len(postype)
    syserr_set2zero = 1 if fix_ratio < 0.2 else 0
    if syserr_set2zero:
        print("Fix ratio is too low, cannot calculate system error.\n")

    syserr_keys = ["x", "y", "alt", "roll", "pitch", "heading"]
    input_keys = ["cal_pos_syserr", "cal_pos_syserr", "cal_alt_syserr", "cal_att_syserr", "cal_att_syserr", "cal_att_syserr"]
    usr_def_keys = ["usr_def_syserr_x", "usr_def_syserr_y", "usr_def_syserr_z", "usr_def_syserr_r", "usr_def_syserr_p", "usr_def_syserr_h"]
    data = [x, y, alt, roll, pitch, heading]

    for i, key in enumerate(syserr_keys):
        if_cal_syserr = syserr_set2zero + input_cfg[input_keys[i]] + input_cfg[usr_def_keys[i]]
        if if_cal_syserr == -1:
            data_fix = data[i][postype == 1]
            syserr[key] = syserr_cal_alg(data_fix)
        elif if_cal_syserr in [1, 2, 5, 6]:
            syserr[key] = input_cfg["usr_def_syserr_list"][i]
        else:
            print(f"System error of {key} is not calculated, set to zero\n")

    return syserr


__all__ = ['wgs84_to_enu', 'wgs84_to_utm', 'get_distance', 'check_deg', 'get_syserr']
