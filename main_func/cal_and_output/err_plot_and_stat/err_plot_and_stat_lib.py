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
        'sig1': round(err[row1 - 1][0], 4),  # Python index starts from 0
        'sig2': round(err[row2 - 1][0], 4),
        'sig3': round(err[row3 - 1][0], 4)
    }

    return sig_count


def fig_plt(xaxis_list, yaxis_list, title: list, xlabel: str, ylabel: str, fig_path: str, *args: list, **kwargs):
    i = len(yaxis_list)
    fig, ax = plt.subplots(i, 1, figsize=(19.2, 10.8))
    for i, yaxis_idct in enumerate(yaxis_list):
        for xaxis_dev, yaxis_dev, color_inturn in zip(xaxis_list, yaxis_idct, color_lib.values()):
            ax[i].plot(xaxis_dev, yaxis_dev, color=color_inturn, linewidth=0.5)
        ax[i].ticklabel_format(axis='x', style='plain')
        ax[i].set_title(title[i], fontdict={'family': 'Microsoft YaHei', 'size': 16, 'weight': 'bold'})
        ax[i].set_xlabel(xlabel, fontdict={'family': 'Microsoft YaHei', 'size': 14})
        ax[i].set_ylabel(ylabel, fontdict={'family': 'Microsoft YaHei', 'size': 14})
        ax[i].grid(color='lightgray', linestyle='-', linewidth=0.5)
        if len(kwargs) > 0 and kwargs['is_multiplot']:
            ax[i].legend(args[0])
    fig.tight_layout()
    fig.savefig(fig_path, dpi=300, bbox_inches='tight', format='png')
    plt.close(fig)


def cal_err_with_ev(errlist: np.ndarray, time_array: np.ndarray, dis_array: np.ndarray) -> dict:
    # 时间特征值
    ev_time_key = [10, 30, 60, 120]
    # 距离特征值
    ev_dis_key = [500, 1000, 2000]

    dr_time_dict = {f'{k}s': '' for k in ev_time_key}
    dr_dis_dict = {f'{k}m': '' for k in ev_dis_key}

    time_diff = time_array[-1] - time_array[0]
    dis_diff = dis_array[-1] - dis_array[0]

    for i, seg in enumerate(ev_time_key):
        if time_diff < seg:
            for j in range(i + 1):
                dr_time_dict[f'{ev_time_key[j]}s'] = np.max(errlist[0: np.where(time_array <= time_array[0] + ev_time_key[j])[0][-1]])
            break
        else:
            for seg in ev_time_key:
                dr_time_dict[f'{seg}s'] = np.max(errlist[0: np.where(time_array <= time_array[0] + seg)[0][-1]])

    for i, seg in enumerate(ev_dis_key):
        if dis_diff < seg:
            for j in range(i + 1):
                dr_dis_dict[f'{ev_dis_key[j]}m'] = np.max(errlist[0: np.where(dis_array <= dis_array[0] + ev_dis_key[j])[0][-1]])
            break
        else:
            for seg in ev_dis_key:
                dr_dis_dict[f'{seg}m'] = np.max(errlist[0: np.where(dis_array <= dis_array[0] + seg)[0][-1]])

    return dr_time_dict, dr_dis_dict


def err_time_plot_stat(errlist_scn, path_scene, scene_name, input_cfg) -> np.ndarray:
    if input_cfg['output_fig']:
        # 生成场景误差时间图像
        fig_xy_path = join(path_scene, f'{scene_name}_xy.png')
        fig_pos_alt_path = join(path_scene, f'{scene_name}_pos_alt.png')
        fig_vel_path = join(path_scene, f'{scene_name}_vel.png')
        fig_att_path = join(path_scene, f'{scene_name}_att.png')
        # 输出横纵向误差图像
        fig_plt(
            [errlist_scn[:, [1]]],
            [[errlist_scn[:, [2]]], [errlist_scn[:, [3]]]],
            ['横向误差', '纵向误差'],
            'Time/s',
            '/m',
            fig_xy_path
        )
        # 输出水平、高程误差图像
        fig_plt(
            [errlist_scn[:, [1]]],
            [[errlist_scn[:, [11]]], [errlist_scn[:, [4]]]],
            ['水平误差', '高程误差'],
            'Time/s',
            '/m',
            fig_pos_alt_path
        )
        # 输出速度误差图像
        fig_plt(
            [errlist_scn[:, [1]]],
            [[errlist_scn[:, [5]]], [errlist_scn[:, [6]]], [errlist_scn[:, [7]]]],
            ['ve误差', 'vn误差', 'vu误差'],
            'Time/s',
            '/(m/s)',
            fig_vel_path
        )
        # 输出姿态角误差图像
        fig_plt(
            [errlist_scn[:, [1]]],
            [[errlist_scn[:, [8]]], [errlist_scn[:, [9]]], [errlist_scn[:, [10]]]],
            ['横滚角误差', '俯仰角误差', '航向角误差'],
            'Time/s',
            '/°',
            fig_att_path
        )

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
        'pos': round(np.max(np.abs(errlist_scn[:, [11]])), 4),
        'x': round(np.max(np.abs(errlist_scn[:, [2]])), 4),
        'y': round(np.max(np.abs(errlist_scn[:, [3]])), 4),
        'alt': round(np.max(np.abs(errlist_scn[:, [4]])), 4),
        've': round(np.max(np.abs(errlist_scn[:, [5]])), 4),
        'vn': round(np.max(np.abs(errlist_scn[:, [6]])), 4),
        'vu': round(np.max(np.abs(errlist_scn[:, [7]])), 4),
        'roll': round(np.max(np.abs(errlist_scn[:, [8]])), 4),
        'pitch': round(np.max(np.abs(errlist_scn[:, [9]])), 4),
        'heading': round(np.max(np.abs(errlist_scn[:, [10]])), 4)
    }
    distance = round(errlist_scn[-1, 12] - errlist_scn[0, 12], 2)
    fix_ratio = round(np.sum(errlist_scn[:, [13]] == 1) / len(errlist_scn) * 100, 2)

    # 生成误差统计列表
    L_x = np.array([
        ['横向误差'],
        [SIGMA['x']['sig1']],
        [SIGMA['x']['sig2']],
        [SIGMA['x']['sig3']],
        [RMS['x']],
        [MAX['x']]
    ])
    L_y = np.array([
        ['纵向误差'],
        [SIGMA['y']['sig1']],
        [SIGMA['y']['sig2']],
        [SIGMA['y']['sig3']],
        [RMS['y']],
        [MAX['y']]
    ])
    L_alt = np.array([
        ['高程误差'],
        [SIGMA['alt']['sig1']],
        [SIGMA['alt']['sig2']],
        [SIGMA['alt']['sig3']],
        [RMS['alt']],
        [MAX['alt']]
    ])
    L_pos = np.array([
        ['水平误差'],
        [SIGMA['pos']['sig1']],
        [SIGMA['pos']['sig2']],
        [SIGMA['pos']['sig3']],
        [RMS['pos']],
        [MAX['pos']]
    ])
    L_ve = np.array([
        ['ve误差'],
        [SIGMA['ve']['sig1']],
        [SIGMA['ve']['sig2']],
        [SIGMA['ve']['sig3']],
        [RMS['ve']],
        [MAX['ve']]
    ])
    L_vn = np.array([
        ['vn误差'],
        [SIGMA['vn']['sig1']],
        [SIGMA['vn']['sig2']],
        [SIGMA['vn']['sig3']],
        [RMS['vn']],
        [MAX['vn']]
    ])
    L_vu = np.array([
        ['vu误差'],
        [SIGMA['vu']['sig1']],
        [SIGMA['vu']['sig2']],
        [SIGMA['vu']['sig3']],
        [RMS['vu']],
        [MAX['vu']]
    ])
    L_roll = np.array([
        ['横滚角误差'],
        [SIGMA['roll']['sig1']],
        [SIGMA['roll']['sig2']],
        [SIGMA['roll']['sig3']],
        [RMS['roll']],
        [MAX['roll']]
    ])
    L_pitch = np.array([
        ['俯仰角误差'],
        [SIGMA['pitch']['sig1']],
        [SIGMA['pitch']['sig2']],
        [SIGMA['pitch']['sig3']],
        [RMS['pitch']],
        [MAX['pitch']]
    ])
    L_heading = np.array([
        ['航向角误差'],
        [SIGMA['heading']['sig1']],
        [SIGMA['heading']['sig2']],
        [SIGMA['heading']['sig3']],
        [RMS['heading']],
        [MAX['heading']]
    ])
    L_distance = np.array([
        ['总里程'],
        [distance],
        [''],
        [''],
        [''],
        ['']
    ])
    L_fix_ratio = np.array([
        ['固定率'],
        [fix_ratio],
        [''],
        [''],
        [''],
        ['']
    ])
    L_name = np.array([
        ['场景'],
        [scene_name],
        [''],
        [''],
        [''],
        ['']
    ])
    L_title = np.array([
        ['指标'],
        ['1σ'],
        ['2σ'],
        ['3σ'],
        ['RMS'],
        ['MAX']
    ])

    L_scn = np.hstack((L_name, L_title, L_x, L_y, L_alt, L_pos, L_ve, L_vn, L_vu, L_roll, L_pitch, L_heading, L_fix_ratio, L_distance))
    return L_scn


def dr_err_stat(errlist_scn, scene_name):
    # 获取减去30s的时间作为出隧道时间
    turnel_t = errlist_scn[-1, 1] - 30
    # 获取30s前的索引值
    turnel_index = np.searchsorted(errlist_scn[:, 1], turnel_t, side='right')

    time_array = errlist_scn[:turnel_index, 1]
    dis_array = errlist_scn[:turnel_index, 12]
    dr_err_time_x_dict, dr_err_dis_x_dict = cal_err_with_ev(errlist_scn[:turnel_index, 2], time_array, dis_array)
    dr_err_time_y_dict, dr_err_dis_y_dict = cal_err_with_ev(errlist_scn[:turnel_index, 3], time_array, dis_array)
    dr_err_time_alt_dict, dr_err_dis_alt_dict = cal_err_with_ev(errlist_scn[:turnel_index, 4], time_array, dis_array)
    dr_err_time_pos_dict, dr_err_dis_pos_dict = cal_err_with_ev(errlist_scn[:turnel_index, 11], time_array, dis_array)
    dr_err_time_ve_dict, dr_err_dis_ve_dict = cal_err_with_ev(errlist_scn[:turnel_index, 5], time_array, dis_array)
    dr_err_time_vn_dict, dr_err_dis_vn_dict = cal_err_with_ev(errlist_scn[:turnel_index, 6], time_array, dis_array)
    dr_err_time_vu_dict, dr_err_dis_vu_dict = cal_err_with_ev(errlist_scn[:turnel_index, 7], time_array, dis_array)
    dr_err_time_roll_dict, dr_err_dis_roll_dict = cal_err_with_ev(errlist_scn[:turnel_index, 8], time_array, dis_array)
    dr_err_time_pitch_dict, dr_err_dis_pitch_dict = cal_err_with_ev(errlist_scn[:turnel_index, 9], time_array, dis_array)
    dr_err_time_heading_dict, dr_err_dis_heading_dict = cal_err_with_ev(errlist_scn[:turnel_index, 10], time_array, dis_array)

    # 计算出隧道后的恢复固定解时间
    # if round(np.sum(errlist_scn[:turnel_index, [13]] == 6) / len(errlist_scn[:turnel_index, [13]]) * 100, 2) > 80:
    index_fix = np.where(errlist_scn[turnel_index:, 13] == 1)[0]
    if len(index_fix) == 0:
        fix_time = '>30s'
    fix_time = errlist_scn[turnel_index + index_fix[0], 1] - errlist_scn[turnel_index, 1]


    # 生成DR误差统计列表
    L_x = np.array([
        ['横向误差'],
        [dr_err_time_x_dict['10s']],
        [dr_err_time_x_dict['30s']],
        [dr_err_time_x_dict['60s']],
        [dr_err_time_x_dict['120s']],
        [dr_err_dis_x_dict['500m']],
        [dr_err_dis_x_dict['1000m']],
        [dr_err_dis_x_dict['2000m']]
    ])
    L_y = np.array([
        ['纵向误差'],
        [dr_err_time_y_dict['10s']],
        [dr_err_time_y_dict['30s']],
        [dr_err_time_y_dict['60s']],
        [dr_err_time_y_dict['120s']],
        [dr_err_dis_y_dict['500m']],
        [dr_err_dis_y_dict['1000m']],
        [dr_err_dis_y_dict['2000m']]
    ])
    L_alt = np.array([
        ['高程误差'],
        [dr_err_time_alt_dict['10s']],
        [dr_err_time_alt_dict['30s']],
        [dr_err_time_alt_dict['60s']],
        [dr_err_time_alt_dict['120s']],
        [dr_err_dis_alt_dict['500m']],
        [dr_err_dis_alt_dict['1000m']],
        [dr_err_dis_alt_dict['2000m']]
    ])
    L_pos = np.array([
        ['水平误差'],
        [dr_err_time_pos_dict['10s']],
        [dr_err_time_pos_dict['30s']],
        [dr_err_time_pos_dict['60s']],
        [dr_err_time_pos_dict['120s']],
        [dr_err_dis_pos_dict['500m']],
        [dr_err_dis_pos_dict['1000m']],
        [dr_err_dis_pos_dict['2000m']]
    ])
    L_ve = np.array([
        ['ve误差'],
        [dr_err_time_ve_dict['10s']],
        [dr_err_time_ve_dict['30s']],
        [dr_err_time_ve_dict['60s']],
        [dr_err_time_ve_dict['120s']],
        [dr_err_dis_ve_dict['500m']],
        [dr_err_dis_ve_dict['1000m']],
        [dr_err_dis_ve_dict['2000m']]
    ])
    L_vn = np.array([
        ['vn误差'],
        [dr_err_time_vn_dict['10s']],
        [dr_err_time_vn_dict['30s']],
        [dr_err_time_vn_dict['60s']],
        [dr_err_time_vn_dict['120s']],
        [dr_err_dis_vn_dict['500m']],
        [dr_err_dis_vn_dict['1000m']],
        [dr_err_dis_vn_dict['2000m']]
    ])
    L_vu = np.array([
        ['vu误差'],
        [dr_err_time_vu_dict['10s']],
        [dr_err_time_vu_dict['30s']],
        [dr_err_time_vu_dict['60s']],
        [dr_err_time_vu_dict['120s']],
        [dr_err_dis_vu_dict['500m']],
        [dr_err_dis_vu_dict['1000m']],
        [dr_err_dis_vu_dict['2000m']]
    ])
    L_roll = np.array([
        ['横滚角误差'],
        [dr_err_time_roll_dict['10s']],
        [dr_err_time_roll_dict['30s']],
        [dr_err_time_roll_dict['60s']],
        [dr_err_time_roll_dict['120s']],
        [dr_err_dis_roll_dict['500m']],
        [dr_err_dis_roll_dict['1000m']],
        [dr_err_dis_roll_dict['2000m']]
    ])
    L_pitch = np.array([
        ['俯仰角误差'],
        [dr_err_time_pitch_dict['10s']],
        [dr_err_time_pitch_dict['30s']],
        [dr_err_time_pitch_dict['60s']],
        [dr_err_time_pitch_dict['120s']],
        [dr_err_dis_pitch_dict['500m']],
        [dr_err_dis_pitch_dict['1000m']],
        [dr_err_dis_pitch_dict['2000m']]
    ])
    L_heading = np.array([
        ['航向角误差'],
        [dr_err_time_heading_dict['10s']],
        [dr_err_time_heading_dict['30s']],
        [dr_err_time_heading_dict['60s']],
        [dr_err_time_heading_dict['120s']],
        [dr_err_dis_heading_dict['500m']],
        [dr_err_dis_heading_dict['1000m']],
        [dr_err_dis_heading_dict['2000m']]
    ])
    L_name = np.array([
        ['场景'],
        [scene_name],
        [''],
        [''],
        [''],
        [''],
        [''],
        ['']
    ])
    L_title = np.array([
        ['指标'],
        ['10s'],
        ['30s'],
        ['60s'],
        ['120s'],
        ['500m'],
        ['1000m'],
        ['2000m']
    ])
    L_fix_time = np.array([
        ['恢复固定解时间'],
        [fix_time],
        [''],
        [''],
        [''],
        [''],
        [''],
        ['']
    ])

    L_dr = np.hstack((L_name, L_title, L_x, L_y, L_alt, L_pos, L_ve, L_vn, L_vu, L_roll, L_pitch, L_heading, L_fix_time))

    return L_dr


def multi_dev_err_plot(err_dict, input_cfg):
    # err_dict: {'dev1': errlist1, 'dev2': errlist2, ...}

    path_multiplt = join(input_cfg['path_proj'], 'multi_dev_err_plot')
    if not exists(path_multiplt):
        makedirs(path_multiplt)
    for i in range(len(input_cfg['era_list'])):
        # 获取场景名称和时间段
        scene_name = input_cfg['era_list'][i]['scene']
        start_t_list = input_cfg['era_list'][i]['era_start'].split(',')
        end_t_list = input_cfg['era_list'][i]['era_end'].split(',')

        # 生成场景子路径
        path_scene = join(path_multiplt, scene_name)
        if not exists(path_scene):
            makedirs(path_scene)

        err_dict_scn = {}

        # 按照设备和开始时间和结束时间划分数据
        for k in input_cfg['data_test']:
            err_scn_list = []
            for j in range(len(start_t_list)):
                start_t = float(start_t_list[j])  # 将start_t从字符串转换为浮点数
                end_t = float(end_t_list[j])  # 将end_t从字符串转换为浮点数
                time_list = err_dict[k['dev_name']][:, 1]
                indx = np.where((time_list >= start_t) & (time_list < end_t))[0]
                err_scn_list.append(err_dict[k['dev_name']][indx])

            # 如果err_scn_list为空，则跳过
            if len(err_scn_list) == 0:
                print('设备{}场景{}数据为空，跳过'.format(k['dev_name'], scene_name))
                continue
            err_dict_scn[k['dev_name']] = np.vstack((err_scn_list))

        # 获取err_dict_scn中的设备名称列表
        scn_dev_name_list = list(err_dict_scn.keys())

        # 生成多设备误差对比图
        fig_xy_path = join(path_scene, f'{scene_name}_xy.png')
        fig_pos_alt_path = join(path_scene, f'{scene_name}_pos_alt.png')
        fig_vel_path = join(path_scene, f'{scene_name}_vel.png')
        fig_att_path = join(path_scene, f'{scene_name}_att.png')
        # 输出横纵向误差图像
        fig_plt([err_dict_scn[k][:, [1]] for k in scn_dev_name_list],
                [[err_dict_scn[k][:, [2]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [3]] for k in scn_dev_name_list]],
                ['横向误差', '纵向误差'],
                'Time/s',
                '/m',
                fig_xy_path,
                scn_dev_name_list,
                is_multiplot=True)
        # 输出水平、高程误差图像
        fig_plt([err_dict_scn[k][:, [1]] for k in scn_dev_name_list],
                [[err_dict_scn[k][:, [11]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [4]] for k in scn_dev_name_list]],
                ['水平误差', '高程误差'],
                'Time/s',
                '/m',
                fig_pos_alt_path,
                scn_dev_name_list,
                is_multiplot=True)
        # 输出速度误差图像
        fig_plt([err_dict_scn[k][:, [1]] for k in scn_dev_name_list],
                [[err_dict_scn[k][:, [5]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [6]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [7]] for k in scn_dev_name_list]],
                ['ve误差', 'vn误差', 'vu误差'],
                'Time/s',
                '/(m/s)',
                fig_vel_path,
                scn_dev_name_list,
                is_multiplot=True)
        # 输出姿态角误差图像
        fig_plt([err_dict_scn[k][:, [1]] for k in scn_dev_name_list],
                [[err_dict_scn[k][:, [8]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [9]] for k in scn_dev_name_list],
                 [err_dict_scn[k][:, [10]] for k in scn_dev_name_list]],
                ['横滚角误差', '俯仰角误差', '航向角误差'],
                'Time/s',
                '/°',
                fig_att_path,
                scn_dev_name_list,
                is_multiplot=True)


__all__ = ['err_time_plot_stat', 'dr_err_stat', 'multi_dev_err_plot']
