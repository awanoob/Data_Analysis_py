# Data decode library
# 以文件路径作为输入，用numpy读取文件数据，返回数据矩阵
# 数据矩阵的格式如下
# gps_week, gps_sec, lat, lon, alt, ve, vn, vu, roll, pitch, yaw, postype, instype, n_sat, gnss_status, std_lat, std_lon, std_alt, std_ve, std_vn, std_vu, std_roll, std_pitch, std_yaw

import numpy as np


# navplot协议数据解析
def decode_navplot(data_path: str) -> np.ndarray:
    # 以空格作为分隔符读取数据
    file_matrix = np.genfromtxt(data_path, delimiter=None, encoding='utf-8')
    # 将特定列的数据提取出来，组成新的数据矩阵
    data_matrix = np.zeros((file_matrix.shape[0], 24))
    data_matrix[:, 0] = file_matrix[:, 0]
    data_matrix[:, 1] = file_matrix[:, 1]
    data_matrix[:, 2] = file_matrix[:, 2]
    data_matrix[:, 3] = file_matrix[:, 3]
    data_matrix[:, 4] = file_matrix[:, 4]
    data_matrix[:, 5] = file_matrix[:, 15]
    data_matrix[:, 6] = file_matrix[:, 16]
    data_matrix[:, 7] = file_matrix[:, 17]
    data_matrix[:, 8] = file_matrix[:, 18]
    data_matrix[:, 9] = file_matrix[:, 19]
    data_matrix[:, 10] = file_matrix[:, 20]
    data_matrix[:, 11] = file_matrix[:, 5]
    data_matrix[:, 12] = file_matrix[:, 14]
    data_matrix[:, 13] = file_matrix[:, 6]
    return data_matrix


__all__ = ['decode_navplot']
