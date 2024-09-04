import numpy as np
from main_func.error_cal.error_cal_lib import *


def err_cal_func(array_bchmk: np.ndarray, array_test: np.ndarray) -> np.ndarray:
    heading_truth = array_bchmk[:, 5]
    n_bchmk = np.zeros((len(heading_truth), 1))
    e_bchmk = np.zeros((len(heading_truth), 1))
    n_test = np.zeros((len(heading_truth), 1))
    e_test = np.zeros((len(heading_truth), 1))
    # 经纬度转横轴墨卡托投影坐标
    e_bchmk, n_bchmk = proj_TM(array_bchmk[:, 2], array_bchmk[:, 3])
    e_test, n_test = proj_TM(array_test[:, 2], array_test[:, 3])
    distance = get_distance(n_bchmk, e_bchmk, array_bchmk[:, 4], array_bchmk[:, ])
