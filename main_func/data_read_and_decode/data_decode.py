from data_read_and_decode.data_aggrement_lib import *
import numpy as np


def _data_decode(data_path: str, data_agg: int) -> np.ndarray:
    # data_agg:
    # 1: navplot协议，分隔符为空格，无数据头，长度27个字段
    # 2: GPCHC协议，分隔符为逗号和*号，数据头为$GPCHC，长度
    if data_agg == 1:
        data_matrix = _decode_navplot(data_path)
    return data_matrix
