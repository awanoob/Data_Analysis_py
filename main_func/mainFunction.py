# Date: 2024-09-01
# Author: Jacob Cheng
# Email: yanqi_cheng@huace.com
# Version: 0.1
# Description: This function is the main function of the project. It is used to call other functions in the project.
# Input: input_cfg: dict, the configuration of the project
from os.path import basename, join
import numpy as np
from data_read_and_decode.data_rnd_lib import *
from error_cal.err_cal import err_cal_func
from err_plot_and_stat.err_plot_and_stat_lib import *
from report_output.report_gen import report_gen_func


def mainFunc(input_cfg: dict):
    if input_cfg['output_multi_fig']:
        multi_dev_err_dict = {k: np.array([]) for k in input_cfg['dev_name_list']}
    for i in range(len(input_cfg['path_in_list'])):
        # 根据被测数据文件名称生成项目子路径
        proj_path_dev = join(input_cfg['path_proj'], basename(input_cfg['path_in_list'][i]).split('.')[0])
        # 基准设备数据读取
        array_bchmk_ori = data_decode(input_cfg['path_truth'], input_cfg['data_agg_truth'])
        # 测试设备数据读取
        array_test_ori = data_decode(input_cfg['path_in_list'][i], input_cfg['data_agg_list'][i])

        # 将非navplot格式的数据转换为navplot格式输出
        if input_cfg['cvrt2navplot']:
            if input_cfg['data_agg_truth'] != 1 and i == 0:
                nav_output_path_bchmk = join(proj_path_dev, 'bchmk.navplot')
                output_navplot(array_bchmk_ori, nav_output_path_bchmk)
            if input_cfg['data_agg_list'][i] != 1:
                nav_output_path_test = join(proj_path_dev, 'test.navplot')
                output_navplot(array_test_ori, nav_output_path_test)

        # 检查数据丢包
        if input_cfg['data_frq_truth'] is not None:
            itv_chk_report_path = join(input_cfg['path_proj'], 'itv_chk_report_bchmk.txt')
            pack_lost_chk(array_bchmk_ori, input_cfg['data_frq_truth'], itv_chk_report_path)
        if input_cfg['data_frq_list'][i] is not None:
            itv_chk_report_path = join(proj_path_dev, 'itv_chk_report_test.txt')
            pack_lost_chk(array_test_ori, input_cfg['data_frq_list'][i], itv_chk_report_path)

        # 匹配相同时间戳的行
        indx_common = np.intersect1d(array_bchmk_ori[:, 1], array_test_ori[:, 1])
        array_bchmk = array_bchmk_ori[np.isin(array_bchmk_ori[:, 1], indx_common)]
        array_test = array_test_ori[np.isin(array_test_ori[:, 1], indx_common)]
        # 计算误差
        errlist = err_cal_func(array_bchmk, array_test, input_cfg)
        multi_dev_err_dict[input_cfg['dev_name_list'][i]] = errlist

        # 输出误差时间图像和统计报告
        err_time_plot_stat(errlist, proj_path_dev, input_cfg)

        # 输出固定解，浮动解误差时间图像和统计报告
        fix_float_err_time_plot_stat(errlist, proj_path_dev, input_cfg)

        # 输出DR误差统计
        dr_err_stat(errlist, proj_path_dev, input_cfg)

    if input_cfg['output_multi_fig']:
        # 输出多设备误差对比图
        multi_dev_err_plot(multi_dev_err_dict, input_cfg)

    # 输出报告
    report_gen_func()


if __name__ == '__main__':
    mainFunc()
