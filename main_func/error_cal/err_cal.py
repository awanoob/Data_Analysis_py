import numpy as np
from error_cal.error_cal_lib import *


def err_cal_func(array_bchmk: np.ndarray, array_test: np.ndarray, input_cfg: dict) -> np.ndarray:
    heading_truth = -np.deg2rad(array_bchmk[:, [5]])
    n_bchmk = np.zeros((len(heading_truth), 1))
    e_bchmk = np.zeros((len(heading_truth), 1))
    n_test = np.zeros((len(heading_truth), 1))
    e_test = np.zeros((len(heading_truth), 1))
    # 经纬度转横轴墨卡托投影坐标
    e_bchmk, n_bchmk = wgs84_to_utm(array_bchmk[:, [2]], array_bchmk[:, [3]])
    e_test, n_test = wgs84_to_utm(array_test[:, [2]], array_test[:, [3]])
    distance = get_distance(n_bchmk, e_bchmk, array_bchmk[:, [4]], array_bchmk[:, [5]], array_bchmk[:, [6]])
    # 东向、北向和天向误差
    # err_e = e_test - e_bchmk
    # err_n = n_test - n_bchmk
    # err_alt = array_test[:, [4]] - array_bchmk[:, [4]]
    err_e, err_n, err_alt = wgs84_to_enu(array_test[:, [2]], array_test[:, [3]], array_test[:, [4]], array_bchmk[:, [2]], array_bchmk[:, [3]], array_bchmk[:, [4]])
    # 将东北向误差旋转到车辆坐标系的横纵向误差
    err_x = err_e * np.cos(heading_truth) + err_n * np.sin(heading_truth)  # 横向误差
    err_y = err_n * np.cos(heading_truth) - err_e * np.sin(heading_truth)  # 纵向误差
    # 速度误差
    err_ve = array_test[:, [5]] - array_bchmk[:, [5]]
    err_vn = array_test[:, [6]] - array_bchmk[:, [6]]
    err_vu = array_test[:, [7]] - array_bchmk[:, [7]]
    # 姿态角误差
    err_roll = array_test[:, [8]] - array_bchmk[:, [8]]
    err_pitch = array_test[:, [9]] - array_bchmk[:, [9]]
    err_heading = check_deg(array_test[:, [10]] - array_bchmk[:, [10]])

    # 计算系统误差
    syserr = get_syserr(err_x, err_y, err_alt, err_roll, err_pitch, err_heading, input_cfg, array_test[:, [11]])
    print(syserr)

    # 去除系统误差
    if input_cfg["out2car_coor"]:
        err_x = err_x - syserr["x"]
        err_y = err_y - syserr["y"]
    else:
        err_x_t = err_x - syserr["x"]
        err_y_t = err_y - syserr["y"]
        err_x = err_x_t * np.cos(-heading_truth) + err_y_t * np.sin(-heading_truth)
        err_y = err_y_t * np.cos(-heading_truth) - err_x_t * np.sin(-heading_truth)
    err_pos = np.sqrt(np.power(err_x, 2) + np.power(err_y, 2))
    err_alt = err_alt - syserr["alt"]
    err_roll = err_roll - syserr["roll"]
    err_pitch = err_pitch - syserr["pitch"]
    err_heading = err_heading - syserr["heading"]

    errlist = np.hstack((array_bchmk[:, [0]], array_bchmk[:, [1]], err_x, err_y, err_alt, err_ve, err_vn, err_vu, err_roll, err_pitch, err_heading, err_pos, distance, array_test[:, [11]], array_test[:, [13]], array_test[:, [14]], e_test, n_test))

    return errlist
