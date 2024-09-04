import numpy as np


def _output_navplot(data_matrix: np.ndarray, output_path: str):
    # 将数据矩阵写入文件
    format = '%d,%.2f,%.8f,%.8f,%.3f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f'
    navplot_matrix = np.hstack((data_matrix[:, [0, 1, 2, 3, 4, 11, 13]], np.zeros((data_matrix.shape[0], 7)), data_matrix[:, [12, 5, 6, 7, 8, 9, 10]]))
    np.savetxt(output_path, navplot_matrix, fmt=format, delimiter=' ')
