import numpy as np
import datetime

def get_sigma(err, app):
    try:
        err = np.abs(err)
        err = np.sort(err)
        row_len = len(err)

        if app.SettingOpt.outputCEPNode == 1:
            sigma1, sigma2, sigma3 = 0.6826, 0.9544, 0.9974
            row1, row2, row3 = round(row_len * sigma1), round(row_len * sigma2), round(row_len * sigma3)
        else:
            row1, row2, row3 = round(row_len * 0.68), round(row_len * 0.95), round(row_len * 0.99)

        sig_count = {
            'sig1': err[row1 - 1],  # Python index starts from 0
            'sig2': err[row2 - 1],
            'sig3': err[row3 - 1]
        }

        return sig_count

    except Exception as e:
        errfile, errname, errline = e.__traceback__.tb_frame.f_code.co_filename, e.__traceback__.tb_frame.f_code.co_name, e.__traceback__.tb_lineno
        err_str = f"{datetime.datetime.now()} ERROR: {e}\nin {errfile}, function: {errname} line: {errline}"
        addlog(app, err_str)


def addlog(app, message):
    print(message)


import numpy as np
import pandas as pd
from datetime import datetime


def errorcount(start, fin, errlist, name, app):
    try:
        # 获取所有时间段内的数据
        errlist_scene = []
        for i in range(len(start)):
            errlist_scene.extend(getdata_bytime(start[i], fin[i], errlist, app))

        errlist_scene = np.array(errlist_scene)

        # 如果数据为空，写日志并返回
        if errlist_scene.size == 0:
            err_str = f"{datetime.now()} Warning:场景{name}时间未包含在数据中"
            addlog(app, err_str)
            return None

        # 提取各个字段数据
        time = errlist_scene[:, 0]
        delta_x_car = errlist_scene[:, 1]
        delta_y_car = errlist_scene[:, 2]
        delta_alt = errlist_scene[:, 3]
        delta_pos = errlist_scene[:, 15]
        delta_yaw_plot = errlist_scene[:, 4]
        delta_pitch = errlist_scene[:, 5]
        delta_roll = errlist_scene[:, 6]
        delta_ve = errlist_scene[:, 7]
        delta_vn = errlist_scene[:, 8]
        delta_vu = errlist_scene[:, 9]
        delta_v = errlist_scene[:, 11]
        distance = errlist_scene[-1, 14] - errlist_scene[0, 14]
        ratio = np.sum(errlist_scene[:, 10] == 1) / len(errlist_scene)
        fix_ratio = ratio * 100

        # 计算RMS值
        RMS = {
            'pos': rms(delta_pos),
            'x_car': rms(delta_x_car),
            'y_car': rms(delta_y_car),
            'alt': rms(delta_alt),
            'yaw': rms(delta_yaw_plot),
            'pitch': rms(delta_pitch),
            'roll': rms(delta_roll),
            've': rms(delta_ve),
            'vn': rms(delta_vn),
            'vu': rms(delta_vu),
            'v': rms(delta_v)
        }

        # 获取1σ至3σ
        sig_count_pos = get_sigma(delta_pos, app)
        sig_count_x_car = get_sigma(delta_x_car, app)
        sig_count_y_car = get_sigma(delta_y_car, app)
        sig_count_alt = get_sigma(delta_alt, app)
        sig_count_yaw = get_sigma(delta_yaw_plot, app)
        sig_count_pitch = get_sigma(delta_pitch, app)
        sig_count_roll = get_sigma(delta_roll, app)
        sig_count_ve = get_sigma(delta_ve, app)
        sig_count_vn = get_sigma(delta_vn, app)
        sig_count_vu = get_sigma(delta_vu, app)
        sig_count_v = get_sigma(delta_v, app)

        # 获取最大、最小和平均值
        data_extrem_pos = extrem_count(delta_pos)
        data_extrem_x_car = extrem_count(delta_x_car)
        data_extrem_y_car = extrem_count(delta_y_car)
        data_extrem_alt = extrem_count(delta_alt)
        data_extrem_yaw = extrem_count(delta_yaw_plot)
        data_extrem_pitch = extrem_count(delta_pitch)
        data_extrem_roll = extrem_count(delta_roll)
        data_extrem_ve = extrem_count(delta_ve)
        data_extrem_vn = extrem_count(delta_vn)
        data_extrem_vu = extrem_count(delta_vu)
        data_extrem_v = extrem_count(delta_v)

        # 汇总统计量
        L_pos = ['水平误差', sig_count_pos['sig1'], sig_count_pos['sig2'], sig_count_pos['sig3'],
                 data_extrem_pos['maxi'], data_extrem_pos['mini'], data_extrem_pos['ave'], RMS['pos']]
        L_x_car = ['纵向误差', sig_count_x_car['sig1'], sig_count_x_car['sig2'], sig_count_x_car['sig3'],
                   data_extrem_x_car['maxi'], data_extrem_x_car['mini'], data_extrem_x_car['ave'], RMS['x_car']]
        L_y_car = ['横向误差', sig_count_y_car['sig1'], sig_count_y_car['sig2'], sig_count_y_car['sig3'],
                   data_extrem_y_car['maxi'], data_extrem_y_car['mini'], data_extrem_y_car['ave'], RMS['y_car']]
        L_alt = ['高程误差', sig_count_alt['sig1'], sig_count_alt['sig2'], sig_count_alt['sig3'],
                 data_extrem_alt['maxi'], data_extrem_alt['mini'], data_extrem_alt['ave'], RMS['alt']]
        L_yaw = ['航向角误差', sig_count_yaw['sig1'], sig_count_yaw['sig2'], sig_count_yaw['sig3'],
                 data_extrem_yaw['maxi'], data_extrem_yaw['mini'], data_extrem_yaw['ave'], RMS['yaw']]
        L_pitch = ['俯仰角误差', sig_count_pitch['sig1'], sig_count_pitch['sig2'], sig_count_pitch['sig3'],
                   data_extrem_pitch['maxi'], data_extrem_pitch['mini'], data_extrem_pitch['ave'], RMS['pitch']]
        L_roll = ['横滚角误差', sig_count_roll['sig1'], sig_count_roll['sig2'], sig_count_roll['sig3'],
                  data_extrem_roll['maxi'], data_extrem_roll['mini'], data_extrem_roll['ave'], RMS['roll']]
        L_ve = ['东向速度误差', sig_count_ve['sig1'], sig_count_ve['sig2'], sig_count_ve['sig3'],
                data_extrem_ve['maxi'], data_extrem_ve['mini'], data_extrem_ve['ave'], RMS['ve']]
        L_vn = ['北向速度误差', sig_count_vn['sig1'], sig_count_vn['sig2'], sig_count_vn['sig3'],
                data_extrem_vn['maxi'], data_extrem_vn['mini'], data_extrem_vn['ave'], RMS['vn']]
        L_vu = ['天向速度误差', sig_count_vu['sig1'], sig_count_vu['sig2'], sig_count_vu['sig3'],
                data_extrem_vu['maxi'], data_extrem_vu['mini'], data_extrem_vu['ave'], RMS['vu']]
        L_v = ['速度误差', sig_count_v['sig1'], sig_count_v['sig2'], sig_count_v['sig3'],
               data_extrem_v['maxi'], data_extrem_v['mini'], data_extrem_v['ave'], RMS['v']]
        L_ratio = ['固定率', fix_ratio, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        L_dis = ['距离', distance, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        L_name = ['场景', name, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
        L_title = ['统计量', '1σ/CEP68', '2σ/CEP95', '3σ/CEP99', 'max', 'min', 'ave', 'RMS']

        # 汇总结果
        L = [L_name, L_title, L_y_car, L_x_car, L_alt, L_pos, L_ve, L_vn, L_vu, L_v, L_yaw, L_roll, L_pitch, L_ratio,
             L_dis]

        # 返回结果
        return L

    except Exception as e:
        errfile = e.__traceback__.tb_frame.f_code.co_filename
        errname = e.__traceback__.tb_frame.f_code.co_name
        errline = e.__traceback__.tb_lineno
        err_str = f"{datetime.now()} ERROR: {str(e)}\nin {errfile}, function: {errname} line: {errline}"
        addlog(app, err_str)
        return None


# 将多个场景的统计量合并并保存为CSV
def save_scenario_data_to_csv(all_scenarios, output_file):
    # 将所有场景的统计量合并
    combined_data = []
    for scenario in all_scenarios:
        combined_data.extend(scenario)

    # 转换为DataFrame并保存为CSV
    df = pd.DataFrame(combined_data)
    df.to_csv(output_file, index=False, header=False)

