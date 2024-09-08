import numpy as np
from os.path import join, exists
from os import makedirs
from data_read_and_decode.data_rnd_lib import output_navplot
from err_plot_and_stat.err_plot_and_stat_lib import *


def result_gen_func(array_bchmk: np.ndarray, array_test: np.ndarray, errlist: np.ndarray, path_main: str, input_cfg: dict):
    for i in range(len(input_cfg['era_list']['Scene'])):
        # 获取场景名称和时间段
        scene_name = input_cfg['era_list']['Scene'][i]
        start_t_list = input_cfg['era_list']['start_time'][i]
        end_t_list = input_cfg['era_list']['end_time'][i]

        # 生成场景子路径
        path_scene = join(path_main, scene_name)
        if not exists(path_scene):
            makedirs(path_scene)

        array_bchmk_scn = np.array([])
        array_test_scn = np.array([])
        errlist_scn = np.array([])

        # 按照开始时间和结束时间划分数据
        for j in range(len(start_t_list)):
            start_t = start_t_list[j]
            end_t = end_t_list[j]
            indx = np.where((array_bchmk[:, 1] >= start_t) & (array_bchmk[:, 1] < end_t))[0]
            np.vstack((array_bchmk_scn, array_bchmk[indx]))
            np.vstack((array_test_scn, array_test[indx]))
            np.vstack((errlist_scn, errlist[indx]))

        # 输出单场景navplot文件
        output_navplot(array_bchmk_scn, join(path_scene, f"{scene_name}_bchmk.navplot"))
        output_navplot(array_test_scn, join(path_scene, f"{scene_name}_test.navplot"))

        # 输出单场景误差时间图像和统计报告
        err_time_plot_stat(errlist_scn, path_scene, scene_name, input_cfg)

        # 输出单场景固定解，浮动解误差时间图像和统计报告
        fix_float_err_time_plot_stat(errlist_scn, path_scene, scene_name, input_cfg)

        # 判断是否为隧道场景，并输出单场景DR误差统计，隧道场景特征为测试数据的搜星数为0的占比大于0.75
        # 如果没有搜星数这个字段咋办？
        if np.count_nonzero(array_test_scn[:, 13] == 0) / len(array_test_scn) <= 0.25:

            errlist_scn = errlist[np.where((array_bchmk[:, 1] >= start_t) & (array_bchmk[:, 1] < end_t + 30))[0]]
            dr_err_stat(errlist_scn, path_scene, scene_name, input_cfg)
    pass
