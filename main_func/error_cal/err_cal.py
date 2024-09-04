import numpy as np
from main_func.error_cal.proj_TM import _proj_TM


def _err_cal(array_bchmk: np.ndarray, array_test: np.ndarray) -> list:
    heading_truth = array_bchmk[:, 5]
    n_bchmk = np.zeros((len(heading_truth), 1))
    e_bchmk = np.zeros((len(heading_truth), 1))
    n_test = np.zeros((len(heading_truth), 1))
    e_test = np.zeros((len(heading_truth), 1))
    # 经纬度转横轴墨卡托投影坐标
    for i in range(len(heading_truth)):
        n_bchmk[i], e_bchmk[i] = _proj_TM(array_bchmk[i, 2], array_bchmk[i, 3])
        n_test[i], e_test[i] = _proj_TM(array_test[i, 2], array_test[i, 3])
    distance = _get_distance(n_bchmk, e_bchmk, array_bchmk[:, 4], array_bchmk[:, ])
