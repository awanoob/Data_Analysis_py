import numpy as np
from os.path import join, exists
from os import makedirs
from data_read_and_decode.data_rnd_lib import output_navplot
from err_plot_and_stat.err_plot_and_stat_lib import *
import pandas as pd


def result_gen_func(array_bchmk: np.ndarray, array_test: np.ndarray, errlist: np.ndarray, path_main: str, input_cfg: dict):
    L_all = np.empty((0, 14))
    L_fix_all = np.empty((0, 14))
    L_float_all = np.empty((0, 14))
    dev_name = path_main.split('\\')[-1]
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
            indx = np.where((array_bchmk[:, [1]] >= start_t) & (array_bchmk[:, [1]] < end_t))[0]
            np.vstack((array_bchmk_scn, array_bchmk[indx]))
            np.vstack((array_test_scn, array_test[indx]))
            np.vstack((errlist_scn, errlist[indx]))

        # 输出单场景navplot文件
        output_navplot(array_bchmk_scn, join(path_scene, f"{scene_name}_bchmk.navplot"))
        output_navplot(array_test_scn, join(path_scene, f"{scene_name}_test.navplot"))

        # 输出单场景误差时间图像和统计报告
        path_fig_stat = join(path_scene, 'fig_stat')
        if not exists(path_fig_stat):
            makedirs(path_fig_stat)
        L_scn = err_time_plot_stat(errlist_scn, path_fig_stat, scene_name, input_cfg)
        L_all = np.vstack((L_all, L_scn))

        # 输出单场景固定解，浮动解误差时间图像和统计报告
        if errlist_scn[:, [13]].all() == 1 or np.sum(errlist_scn[:, [13]] == 6) / len(errlist_scn) > 0.8:
            L_fix_scn = np.empty((0, 14))
            L_fix_all = np.vstack((L_fix_all, L_fix_scn))
            L_float_scn = np.empty((0, 14))
            L_float_all = np.vstack((L_float_all, L_float_scn))
        else:
            path_ff_fig_stat = join(path_scene, 'ff_fig_stat')
            if not exists(path_ff_fig_stat):
                makedirs(path_ff_fig_stat)
            errlist_fix_scn = errlist_scn[np.where(errlist_scn[:, [13]] == 1)[0]]
            errlist_float_scn = errlist_scn[np.where(errlist_scn[:, [13]] == 2)[0]]
            L_fix_scn = err_time_plot_stat(errlist_fix_scn, path_ff_fig_stat, f'{scene_name}_fix', input_cfg)
            L_float_scn = err_time_plot_stat(errlist_float_scn, path_ff_fig_stat, f'{scene_name}_float', input_cfg)
            L_fix_all = np.vstack((L_fix_all, L_fix_scn))
            L_float_all = np.vstack((L_float_all, L_float_scn))    

        # 判断是否为隧道场景，并输出单场景DR误差统计，隧道场景特征为测试数据的搜星数为0的占比大于0.75
        # 如果没有搜星数这个字段咋办？
        if np.count_nonzero(array_test_scn[:, [13]] == 0) / len(array_test_scn) <= 0.25:

            errlist_scn = errlist[np.where((array_bchmk[:, [1]] >= start_t) & (array_bchmk[:, [1]] < end_t + 30))[0]]
            dr_err_stat(errlist_scn, path_scene, scene_name, input_cfg)

    # 将ndarray转换为DataFrame
    L_all = pd.DataFrame(L_all)
    L_fix_all = pd.DataFrame(L_fix_all)
    L_float_all = pd.DataFrame(L_float_all)


    # 输出统计表
    L_all.to_csv(join(path_main, f'{dev_name}_误差统计表.csv'), index=False)
    L_fix_all.to_csv(join(path_main, f'{dev_name}_固定解误差统计表.csv'), index=False)
    L_float_all.to_csv(join(path_main, f'{dev_name}_浮动解误差统计表.csv'), index=False)
