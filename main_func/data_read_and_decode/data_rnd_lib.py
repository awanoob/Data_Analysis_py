from data_read_and_decode.data_aggrement_lib import *
import numpy as np


def data_decode(data_path: str, data_agg: int) -> np.ndarray:
    # data_agg:
    # 1: navplot协议，分隔符为空格，无数据头，长度27个字段
    # 2: GPCHC协议，分隔符为逗号和*号，数据头为$GPCHC，长度
    if data_agg == 1:
        data_matrix = decode_navplot(data_path)
    return data_matrix


def output_navplot(data_matrix: np.ndarray, output_path: str):
    # 将数据矩阵写入文件
    format = '%d,%.2f,%.8f,%.8f,%.3f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f'
    navplot_matrix = np.hstack((data_matrix[:, [0, 1, 2, 3, 4, 11, 13]], np.zeros((data_matrix.shape[0], 7)),
                                data_matrix[:, [12, 5, 6, 7, 8, 9, 10]]))
    np.savetxt(output_path, navplot_matrix, fmt=format, delimiter=' ')


def pack_lost_chk(data_matrix: np.ndarray, data_frq: int, out_repo_path: str) -> None:
    """
    检查数据丢包
    期望数据包数 = (最后时间戳 - 第一个时间戳) * 数据频率 + 1
    丢包数 = 期望数据包数 - 实际数据包数
    丢包率 = (丢包数 / 期望数据包数) * 100
    :param data_matrix: 数据矩阵
    :param data_frq: 数据频率
    :param out_repo_path: 输出报告路径
    :return: None
    """
    expected_total_packets = int(data_matrix[-1][1] - data_matrix[0][1]) * data_frq + 1
    received_packets = len(data_matrix)
    lost_packets = expected_total_packets - received_packets
    lost_packet_rate = (lost_packets / expected_total_packets) * 100
    with open(out_repo_path, 'w') as f:
        f.write(f'丢包数: {lost_packets}\n')
        f.write(f'丢包率: {lost_packet_rate}%\n')


__all__ = ['data_decode', 'output_navplot', 'pack_lost_chk']
