# Date: 2024-09-20
# Author: Jacob Cheng
# Email: yanqi_cheng@huace.com
# Version: 0.5_beta
# Description: This function is the main function of the project. It is used to call other functions in the project.
# Input: path of yaml.
from os.path import join, exists
from os import makedirs
import numpy as np
from data_read_and_decode.data_rnd_lib import *
from error_cal.err_cal import err_cal_func
from err_plot_and_stat.err_plot_and_stat_lib import *
from err_plot_and_stat.result_gen import result_gen_func
from report_output.report_gen import report_gen_func
from proj_cfg_read import yaml_read


def mainFunc(yaml_path: str):
    input_cfg = yaml_read(yaml_path)
    if len(input_cfg['dev_name_list']) >= 1 and input_cfg['output_multi_fig']:
        multi_dev_err_dict = {k: np.array([]) for k in input_cfg['dev_name_list']}
    # 基准设备数据读取
    array_bchmk_ori = data_decode(input_cfg['path_truth'], input_cfg['data_agg_truth'])
    for i in range(len(input_cfg['path_in_list'])):
        # 根据被测数据文件名称生成项目子路径
        path_proj_dev = join(input_cfg['path_proj'], input_cfg['dev_name_list'][i])
        # 创建项目子路径
        if not exists(path_proj_dev):
            makedirs(path_proj_dev)
        # # 基准设备数据读取
        # array_bchmk_ori = data_decode(input_cfg['path_truth'], input_cfg['data_agg_truth'])
        # 测试设备数据读取
        array_test_ori = data_decode(input_cfg['path_in_list'][i], input_cfg['data_agg_list'][i])

        # 将非navplot格式的数据转换为navplot格式输出
        if input_cfg['cvrt2navplot']:
            if input_cfg['data_agg_truth'] != 1 and i == 0:
                nav_output_path_bchmk = join(path_proj_dev, 'bchmk.navplot')
                output_navplot(array_bchmk_ori, nav_output_path_bchmk)
            if input_cfg['data_agg_list'][i] != 1:
                nav_output_path_test = join(path_proj_dev, 'test.navplot')
                output_navplot(array_test_ori, nav_output_path_test)

        # 检查数据丢包
        if input_cfg['data_frq_truth'] is not None and i == 0:
            itv_chk_report_path = join(input_cfg['path_proj'], 'itv_chk_report_bchmk.txt')
            pack_lost_chk(array_bchmk_ori, input_cfg['data_frq_truth'], itv_chk_report_path)

        if input_cfg['data_frq_list'][i] != '':
            itv_chk_report_path = join(path_proj_dev, 'itv_chk_report_test.txt')
            pack_lost_chk(array_test_ori, input_cfg['data_frq_list'][i], itv_chk_report_path)

        # 匹配相同时间戳的行
        # 提取相同时间戳列的索引
        indx_common, index_common_bool_bchmk, index_common_bool_test = np.intersect1d(array_bchmk_ori[:, [1]], array_test_ori[:, [1]], assume_unique=False, return_indices=True)
        # 提取相同时间戳的行
        array_bchmk = array_bchmk_ori[index_common_bool_bchmk, :]
        array_test = array_test_ori[index_common_bool_test, :]
        # 计算误差
        errlist = err_cal_func(array_bchmk, array_test, input_cfg)

        if 'multi_dev_err_dict' in locals():
            multi_dev_err_dict[input_cfg['dev_name_list'][i]] = errlist

        # 自动添加全程场景
        if input_cfg['era_auto_all']:
            input_cfg['era_list']['Scene'].insert(0, '全程')
            input_cfg['era_list']['start_time'].insert(0, [array_bchmk[0, 1]])
            input_cfg['era_list']['end_time'].insert(0, [array_bchmk[-1, 1]])

        # 生成图像和统计表结果
        result_gen_func(array_bchmk, array_test, errlist, path_proj_dev, input_cfg)

    if 'multi_dev_err_dict' in locals():
        # 输出多设备误差对比图
        multi_dev_err_plot(multi_dev_err_dict, input_cfg)

    # 输出报告
    report_gen_func()


if __name__ == '__main__':
    mainFunc()
