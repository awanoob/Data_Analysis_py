# Date: 2024-09-20
# Author: Jacob Cheng
# Email: yanqi_cheng@huace.com
# Version: 0.5_beta
# Description: This function is the main function of the project. It is used to call other functions in the project.
# Input: path of yaml.
from os.path import join, exists
from os import makedirs
import numpy as np
from cal_and_output.data_read_and_decode.data_rnd_lib import *
from cal_and_output.error_cal.err_cal import err_cal_func
from cal_and_output.err_plot_and_stat.err_plot_and_stat_lib import *
from cal_and_output.err_plot_and_stat.result_gen import result_gen_func
from cal_and_output.report_output.report_gen import report_gen_func
from cal_and_output.proj_cfg_read import yaml_read
import cProfile
import flameprof


def cal_Func(yaml_path: str):
    input_cfg = yaml_read(yaml_path)

    # 拆分data列表，分为真值和被测数据列表，分别读取数据
    # 获取真值数据的索引
    indices = [index for index, d in enumerate(input_cfg['data']) if d.get('is_bchmk') is True]
    if len(indices) == 0:
        print('未设置真值数据，无法进行计算，请检查文件设置')
        return
    if len(indices) > 1:
        print('真值数据设置错误，只能设置一个真值数据，请检查文件设置')
        return
    data_bchmk = input_cfg['data'][indices[0]]
    # 获取被测数据列表
    del input_cfg['data'][indices[0]]
    data_test = input_cfg['data']
    # 添加进input_cfg
    input_cfg['data_bchmk'] = data_bchmk
    input_cfg['data_test'] = data_test

    # 多设备误差对比误差列表字典初始化
    if len(input_cfg['data']) >= 1:
        multi_dev_err_dict = {k['dev_name']: np.array([]) for k in data_test}

    # 基准设备数据读取
    array_bchmk_ori = data_decode(data_bchmk['data_path'], data_bchmk['data_format'])

    for i in range(len(data_test)):
        # 根据被测数据文件名称生成项目子路径
        path_proj_dev = join(input_cfg['path_proj'], 'result_all', data_test[i]['dev_name'])
        # 创建项目子路径
        if not exists(path_proj_dev):
            makedirs(path_proj_dev)
        # 测试设备数据读取
        array_test_ori = data_decode(data_test[i]['data_path'], data_test[i]['data_format'])

        # 将非navplot格式的数据转换为navplot格式输出
        if input_cfg['cvrt2navplot']:
            if data_bchmk['data_format'] != 'navplot' and i == 0:
                nav_output_path_bchmk = join(path_proj_dev, 'bchmk.navplot')
                output_navplot(array_bchmk_ori, nav_output_path_bchmk)
            if data_test[i]['data_format'] != 'navplot':
                nav_output_path_test = join(path_proj_dev, 'test.navplot')
                output_navplot(array_test_ori, nav_output_path_test)

        # 检查数据丢包
        # if data_bchmk['data_frq'] is not None and i == 0:
        #     itv_chk_report_path = join(input_cfg['path_proj'], 'itv_chk_report_bchmk.txt')
        #     pack_lost_chk(array_bchmk_ori, data_bchmk['data_frq'], itv_chk_report_path)

        # if data_test[i]['data_frq'] != '':
        #     itv_chk_report_path = join(path_proj_dev, 'itv_chk_report_test.txt')
        #     pack_lost_chk(array_test_ori, data_test[i]['data_frq'], itv_chk_report_path)

        # 匹配相同时间戳的行
        # 提取相同时间戳列的索引
        indx_common, index_common_bool_bchmk, index_common_bool_test = np.intersect1d(array_bchmk_ori[:, [1]], array_test_ori[:, [1]], assume_unique=False, return_indices=True)
        # 提取相同时间戳的行
        array_bchmk = array_bchmk_ori[index_common_bool_bchmk, :]
        array_test = array_test_ori[index_common_bool_test, :]
        # 计算误差
        errlist = err_cal_func(array_bchmk, array_test, input_cfg)

        if 'multi_dev_err_dict' in locals():
            multi_dev_err_dict[data_test[i]['dev_name']] = errlist

        # 自动添加全程场景
        if input_cfg['era_auto_all']:
            input_cfg['era_list'].append({'scene': '.全程', 'era_start': str(array_bchmk[0, 1]), 'era_end': str(array_bchmk[-1, 1])})

        # 生成图像和统计表结果
        result_gen_func(array_bchmk, array_test, errlist, path_proj_dev, input_cfg)

        # 删除全程场景
        if input_cfg['era_auto_all']:
            input_cfg['era_list'].pop()

    if 'multi_dev_err_dict' in locals():
        # 输出多设备误差对比图
        multi_dev_err_plot(multi_dev_err_dict, input_cfg)

    # 将输出报告需要的参数添加到input_cfg
    input_cfg['multi_dev_err_path'] = input_cfg['path_proj'] + '/multi_dev_err_plot'
    input_cfg['path_proj_dev'] = input_cfg['path_proj'] + '/result_all'
    # 输出报告
    report_gen_func(input_cfg)


# test
if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    cal_Func(r"J:\CODE\VSCode\Python\pytest\D_A_T_2\proj_test\11-22_test1.yaml")
    pr.disable()
    pr.dump_stats('cal_func_1.prof')
