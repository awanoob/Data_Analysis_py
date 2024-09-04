# yaml配置文件参数集合

## 1、路径

```yaml
path_proj: D:\vscode_python\python_proj\.DataAnalysisAPP_py\func_test\proj_path_test # [str] 工程路径
path_in_list: [] # [str] 输入文件路径，列表
path_truth:  # [str] 基准文件路径
path_eracsv:  # [str] 历元文件路径
# path_eraname:  # 图像输出路径
# path_sta_csv_path:  # 输出统计量csv文件路径
```

## 2、数据属性

```yaml
data_agg_list: [1] # [list] 数据协议，列表；1:navplot...(待定)
data_agg_truth: 1 # [int] 基准文件数据协议
data_frq: [10] # [list] 数据频率，列表
data_frq_truth: 10 # [int] 基准数据频率
```

## 3、输入选项

```yaml
era_list: {Scene: ["1","2"], start_time: [[12345],[23456]], end_time: [[12347],[23458]]} # [dict] 手动输入的历元，列表型，内部嵌套字典
cvrt2navplot: true # [bool] 是否将输入数据转换为navplot格式输出
out2car_coor: true # [bool] 是否输出到车辆坐标系
era_auto_all: false # [bool] 是否自动添加全程场景
output_cep: false # [bool] 输出CEP或者σ
output_fig: true # [bool] 是否输出单设备误差时序图
output_multi_fig: true # [bool] 是否输出多设备误差时序图
usr_def_syserr_x: -3 # [enum] 用户是否自定义 x 系统误差 (3:yes,-3:no)
usr_def_syserr_y: -3 # [enum] 用户是否自定义 y 系统误差 (3:yes,-3:no)
usr_def_syserr_z: -3 # [enum] 用户是否自定义 z 系统误差 (3:yes,-3:no)
usr_def_syserr_r: -3 # [enum] 用户是否自定义 r 系统误差 (3:yes,-3:no)
usr_def_syserr_p: -3 # [enum] 用户是否自定义 p 系统误差 (3:yes,-3:no)
usr_def_syserr_h: -3 # [enum] 用户是否自定义 h 系统误差 (3:yes,-3:no)
usr_def_syserr_list: [] # [list] 用户自定义系统误差;x,y,z,r,p,h
cal_pos_syserr: 2 # [enum] 是否计算水平定位误差 (2:yes,-2:no)
cal_alt_syserr: 2 # [enum] 是否计算高程定位误差 (2:yes,-2:no)
cal_att_syserr: 2 # [enum] 是否计算姿态角定位误差 (2:yes,-2:no)
```
