import matplotlib
import matplotlib.pyplot as plt
from os.path import join, exists
from os import makedirs
import numpy as np


def fig_plt(xaxis: np.ndarray, yaxis_list, title: list, xlabel: str, ylabel: str, fig_path: str):
    i = len(yaxis_list)
    fig, ax = plt.subplots(i, 1, figsize=(19.2, 10.8))
    for i in range(len(yaxis_list)):
        ax[i].plot(xaxis, yaxis_list[i], color='#0072BD')
        ax[i].set_title(title[i], fontsize=16)
        ax[i].set_xlabel(xlabel, fontsize=14)
        ax[i].set_ylabel(ylabel, fontsize=14)
        ax[i].grid(color='lightgray', linestyle='-', linewidth=0.5)
    fig.savefig(fig_path, dpi=300, bbox_inches='tight', format='png')


def err_time_plot_stat(errlist_scn, path_scene, scene_name, input_cfg):
    if input_cfg['output_fig']:
        # 生成场景子路径
        path_fig_stat = join(path_scene, 'fig_stat')
        if not exists(path_fig_stat):
            makedirs(path_fig_stat)

        # 生成场景误差时间图像
        fig_xy_path = join(path_fig_stat, f'{scene_name}_xy.png')
        fig_pos_alt_path = join(path_fig_stat, f'{scene_name}_pos_alt.png')
        fig_vel_path = join(path_fig_stat, f'{scene_name}_vel.png')
        fig_att_path = join(path_fig_stat, f'{scene_name}_att.png')
        fig_plt(errlist_scn[:, 1], [errlist_scn[:, 2], errlist_scn[:, 3]], ['横向误差', '纵向误差'], 'Time/s', '/m', fig_xy_path)
        fig_plt(errlist_scn[:, 1], [errlist_scn[:, 11], errlist_scn[:, 4]], ['水平误差', '高程误差'], 'Time/s', '/m', fig_pos_alt_path)
        fig_plt(errlist_scn[:, 1], [errlist_scn[:, 5], errlist_scn[:, 6], errlist_scn[:, 7]], ['ve误差', 'vn误差', 'vu误差'], 'Time/s', '/(m/s)', fig_vel_path)
        fig_plt(errlist_scn[:, 1], [errlist_scn[:, 8], errlist_scn[:, 9], errlist_scn[:, 10]], ['横滚角误差', '俯仰角误差', '航向角误差'], 'Time/s', '/°', fig_att_path)

    # 生成单场景误差统计表
    pass


def fix_float_err_time_plot_stat():
    pass


def dr_err_stat():
    pass


def multi_dev_err_plot():
    pass


__all__ = ['err_time_plot_stat', 'fix_float_err_time_plot_stat', 'dr_err_stat', 'multi_dev_err_plot']
