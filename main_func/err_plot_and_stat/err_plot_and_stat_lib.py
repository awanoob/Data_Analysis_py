import matplotlib
import matplotlib.pyplot as plt
from os.path import join, exists
from os import makedirs
import numpy as np

# matlab color lib
color_lib = {'dark_blue': '#0072BD', 'orange': '#D95319', 'yellow': '#EDB120', 'purple': '#7E2F8E', 'green': '#77AC30', 'light_blue': '#4DBEEE', 'red': '#A2142F', 'black': '#000000'}


def sigma(err: np.ndarray, input_cfg) -> dict:
    err = np.abs(err)
    err = np.sort(err)
    row_len = len(err)

    if input_cfg['output_cep']:
        row1, row2, row3 = round(row_len * 0.68), round(row_len * 0.95), round(row_len * 0.99)
    else:
        sigma1, sigma2, sigma3 = 0.6827, 0.9545, 0.9973
        row1, row2, row3 = round(row_len * sigma1), round(row_len * sigma2), round(row_len * sigma3)

    sig_count = {
        'sig1': round(err[row1 - 1], 4), # Python index starts from 0
        'sig2': round(err[row2 - 1], 4),
        'sig3': round(err[row3 - 1], 4)
    }

    return sig_count


def fig_plt(xaxis: np.ndarray, yaxis_list, title: list, xlabel: str, ylabel: str, fig_path: str, *args: list, **kwargs):
    i = len(yaxis_list)
    fig, ax = plt.subplots(i, 1, figsize=(19.2, 10.8))
    for i, yaxis_idct in enumerate(yaxis_list):
        for yaxis_dev, color_inturn in zip(yaxis_idct, color_lib.values()):
            ax[i].plot(xaxis, yaxis_dev, color=color_inturn)
        ax[i].set_title(title[i], fontsize=16)
        ax[i].set_xlabel(xlabel, fontsize=14)
        ax[i].set_ylabel(ylabel, fontsize=14)
        ax[i].grid(color='lightgray', linestyle='-', linewidth=0.5)
        if len(kwargs) > 0 and kwargs['is_multiplot']:
            ax[i].legend(args[0])
    fig.savefig(fig_path, dpi=300, bbox_inches='tight', format='png')


def cal_err_with_ev()


def err_time_plot_stat(errlist_scn, path_scene, scene_name, input_cfg) -> np.ndarray:
    if input_cfg['output_fig']:
        # 生成场景误差时间图像
        fig_xy_path = join(path_scene, f'{scene_name}_xy.png')
        fig_pos_alt_path = join(path_scene, f'{scene_name}_pos_alt.png')
        fig_vel_path = join(path_scene, f'{scene_name}_vel.png')
        fig_att_path = join(path_scene, f'{scene_name}_att.png')
        fig_plt(errlist_scn[:, [1]], [[errlist_scn[:, [2]]], [errlist_scn[:, [3]]]], ['横向误差', '纵向误差'], 'Time/s', '/m', fig_xy_path)
        fig_plt(errlist_scn[:, [1]], [[errlist_scn[:, [11]]], [errlist_scn[:, [4]]]], ['水平误差', '高程误差'], 'Time/s', '/m', fig_pos_alt_path)
        fig_plt(errlist_scn[:, [1]], [[errlist_scn[:, [5]]], [errlist_scn[:, [6]]], [errlist_scn[:, [7]]]], ['ve误差', 'vn误差', 'vu误差'], 'Time/s', '/(m/s)', fig_vel_path)
        fig_plt(errlist_scn[:, [1]], [[errlist_scn[:, [8]]], [errlist_scn[:, [9]]], [errlist_scn[:, [10]]]], ['横滚角误差', '俯仰角误差', '航向角误差'], 'Time/s', '/°', fig_att_path)

    # 计算统计量
    RMS = {
        'pos': round(np.sqrt(np.mean(np.power(errlist_scn[:, [11]], 2))), 4),
        'x': round(np.sqrt(np.mean(np.power(errlist_scn[:, [2]], 2))), 4),
        'y': round(np.sqrt(np.mean(np.power(errlist_scn[:, [3]], 2))), 4),
        'alt': round(np.sqrt(np.mean(np.power(errlist_scn[:, [4]], 2))), 4),
        've': round(np.sqrt(np.mean(np.power(errlist_scn[:, [5]], 2))), 4),
        'vn': round(np.sqrt(np.mean(np.power(errlist_scn[:, [6]], 2))), 4),
        'vu': round(np.sqrt(np.mean(np.power(errlist_scn[:, [7]], 2))), 4),
        'roll': round(np.sqrt(np.mean(np.power(errlist_scn[:, [8]], 2))), 4),
        'pitch': round(np.sqrt(np.mean(np.power(errlist_scn[:, [9]], 2))), 4),
        'heading': round(np.sqrt(np.mean(np.power(errlist_scn[:, [10]], 2))), 4)
    }

    SIGMA = {
        'pos': sigma(errlist_scn[:, [11]], input_cfg),
        'x': sigma(errlist_scn[:, [2]], input_cfg),
        'y': sigma(errlist_scn[:, [3]], input_cfg),
        'alt': sigma(errlist_scn[:, [4]], input_cfg),
        've': sigma(errlist_scn[:, [5]], input_cfg),
        'vn': sigma(errlist_scn[:, [6]], input_cfg),
        'vu': sigma(errlist_scn[:, [7]], input_cfg),
        'roll': sigma(errlist_scn[:, [8]], input_cfg),
        'pitch': sigma(errlist_scn[:, [9]], input_cfg),
        'heading': sigma(errlist_scn[:, [10]], input_cfg)
    }

    MAX = {
        'pos': round(np.max(errlist_scn[:, [11]]), 4),
        'x': round(np.max(errlist_scn[:, [2]]), 4),
        'y': round(np.max(errlist_scn[:, [3]]), 4),
        'alt': round(np.max(errlist_scn[:, [4]]), 4),
        've': round(np.max(errlist_scn[:, [5]]), 4),
        'vn': round(np.max(errlist_scn[:, [6]]), 4),
        'vu': round(np.max(errlist_scn[:, [7]]), 4),
        'roll': round(np.max(errlist_scn[:, [8]]), 4),
        'pitch': round(np.max(errlist_scn[:, [9]]), 4),
        'heading': round(np.max(errlist_scn[:, [10]]), 4)
    }
    distance = round(errlist_scn[-1, 12] - errlist_scn[0, 12], 2)
    fix_ratio = round(np.sum(errlist_scn[:, [13]] == 1) / len(errlist_scn) * 100, 2)

    # 生成误差统计列表
    L_x = np.array((['横向误差'], [SIGMA['x']['sig1']], [SIGMA['x']['sig2']], [SIGMA['x']['sig3']], [RMS['x']], [MAX['x']]))
    L_y = np.array((['纵向误差'], [SIGMA['y']['sig1']], [SIGMA['y']['sig2']], [SIGMA['y']['sig3']], [RMS['y']], [MAX['y']]))
    L_alt = np.array((['高程误差'], [SIGMA['alt']['sig1']], [SIGMA['alt']['sig2']], [SIGMA['alt']['sig3']], [RMS['alt']], [MAX['alt']]))
    L_pos = np.array((['水平误差'], [SIGMA['pos']['sig1']], [SIGMA['pos']['sig2']], [SIGMA['pos']['sig3']], [RMS['pos']], [MAX['pos']]))
    L_ve = np.array((['ve误差'], [SIGMA['ve']['sig1']], [SIGMA['ve']['sig2']], [SIGMA['ve']['sig3']], [RMS['ve']], [MAX['ve']]))
    L_vn = np.array((['vn误差'], [SIGMA['vn']['sig1']], [SIGMA['vn']['sig2']], [SIGMA['vn']['sig3']], [RMS['vn']], [MAX['vn']]))
    L_vu = np.array((['vu误差'], [SIGMA['vu']['sig1']], [SIGMA['vu']['sig2']], [SIGMA['vu']['sig3']], [RMS['vu']], [MAX['vu']]))
    L_roll = np.array((['横滚角误差'], [SIGMA['roll']['sig1']], [SIGMA['roll']['sig2']], [SIGMA['roll']['sig3']], [RMS['roll']], [MAX['roll']]))
    L_pitch = np.array((['俯仰角误差'], [SIGMA['pitch']['sig1']], [SIGMA['pitch']['sig2']], [SIGMA['pitch']['sig3']], [RMS['pitch']], [MAX['pitch']]))
    L_heading = np.array((['航向角误差'], [SIGMA['heading']['sig1']], [SIGMA['heading']['sig2']], [SIGMA['heading']['sig3']], [RMS['heading']], [MAX['heading']]))
    L_distance = np.array((['总里程'], [distance], [np.nan], [np.nan], [np.nan], [np.nan]))
    L_fix_ratio = np.array((['固定率'], [fix_ratio], [np.nan], [np.nan], [np.nan], [np.nan]))
    L_name = np.array((['场景'], [scene_name], [np.nan], [np.nan], [np.nan], [np.nan]))
    L_title = np.array((['指标'], ['1σ'], ['2σ'], ['3σ'], ['RMS'], ['MAX']))

    L_scn = np.hstack((L_name, L_title, L_x, L_y, L_alt, L_pos, L_ve, L_vn, L_vu, L_roll, L_pitch, L_heading, L_fix_ratio, L_distance))
    return L_scn


def dr_err_stat(errlist_scn, path_scene, scene_name, input_cfg):
    # 获取减去30s的时间作为出隧道时间
    turnel_t = errlist_scn[-1, 1] - errlist_scn[0, 1] - 30
    # 获取30s前的索引值，来获取出隧道时的行驶距离
    turnel_index = np.searchsorted(errlist_scn[:, 1], turnel_t, side='right') - 1

    turnel_dis = errlist_scn[turnel_index, 12] - errlist_scn[0, 12]
    # 时间特征值
    ev_time = ['10s', '30s', '60s', '120s']
    # 距离特征值
    ev_dis = ['0.5km', '1km', '2km']
    # dr_err_time_max = {'10s': 0, '30s': 0, '60s': 0, '120s': 0}
    # dr_err_dis_max = {'0.5km': 0, '1km': 0, '2km': 0}
    
    pass


def multi_dev_err_plot(err_dict, input_cfg):
    # err_dict: {'dev1': errlist1, 'dev2': errlist2, ...}

    path_multiplt = join(input_cfg['path_proj'], 'multi_dev_err_plot')
    if not exists(path_multiplt):
        makedirs(path_multiplt)
    for i in range(len(input_cfg['era_list']['Scene'])):
        # 获取场景名称和时间段
        scene_name = input_cfg['era_list']['Scene'][i]
        start_t_list = input_cfg['era_list']['start_time'][i]
        end_t_list = input_cfg['era_list']['end_time'][i]

        # 生成场景子路径
        path_scene = join(path_multiplt, scene_name)
        if not exists(path_scene):
            makedirs(path_scene)

        err_dict_scn = {k: np.array([]) for k in input_cfg['dev_name_list']}

        # 按照开始时间和结束时间划分数据
        for j in range(len(start_t_list)):
            start_t = start_t_list[j]
            end_t = end_t_list[j]
                
            for k in input_cfg['dev_name_list']:
                time_list = err_dict[k][:, 1]
                indx = np.where((time_list >= start_t) & (time_list < end_t))[0]
                err_dict_scn[k] = np.vstack((err_dict_scn[k], err_dict[k][indx]))

        # 生成多设备误差对比图
        fig_xy_path = join(path_scene, f'{scene_name}_xy.png')
        fig_pos_alt_path = join(path_scene, f'{scene_name}_pos_alt.png')
        fig_vel_path = join(path_scene, f'{scene_name}_vel.png')
        fig_att_path = join(path_scene, f'{scene_name}_att.png')
        fig_plt(err_dict_scn[input_cfg['dev_name_list'][0]][:, [1]], [[err_dict_scn[k][:, [2]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [3]] for k in input_cfg['dev_name_list']]], ['横向误差', '纵向误差'], 'Time/s', '/m', fig_xy_path, input_cfg['dev_name_list'], is_multiplot=True)
        fig_plt(err_dict_scn[input_cfg['dev_name_list'][0]][:, [1]], [[err_dict_scn[k][:, [11]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [4]] for k in input_cfg['dev_name_list']]], ['水平误差', '高程误差'], 'Time/s', '/m', fig_pos_alt_path, input_cfg['dev_name_list'], is_multiplot=True)
        fig_plt(err_dict_scn[input_cfg['dev_name_list'][0]][:, [1]], [[err_dict_scn[k][:, [5]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [6]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [7]] for k in input_cfg['dev_name_list']]], ['ve误差', 'vn误差', 'vu误差'], 'Time/s', '/(m/s)', fig_vel_path, input_cfg['dev_name_list'], is_multiplot=True)
        fig_plt(err_dict_scn[input_cfg['dev_name_list'][0]][:, [1]], [[err_dict_scn[k][:, [8]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [9]] for k in input_cfg['dev_name_list']]], [[err_dict_scn[k][:, [10]] for k in input_cfg['dev_name_list']]], ['横滚角误差', '俯仰角误差', '航向角误差'], 'Time/s', '/°', fig_att_path, input_cfg['dev_name_list'], is_multiplot=True)


__all__ = ['err_time_plot_stat', 'dr_err_stat', 'multi_dev_err_plot']
