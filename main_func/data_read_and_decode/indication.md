# \data_read_and_decode
进行数据文件的读取和解析，输出数据字段列表，包含gps周、时间、经纬度、速度、姿态、解状态、搜星数、组合状态、纯卫导状态以及预留位
## 读取
数据文件读取支持多种协议，可暂时只支持ascii格式文件读取
## 解析
数据协议中的经纬度等信息的位数，以字典形式存储，字典中包含分隔符、数据头等数据协议读取所需参数
## 输出
当输入的文件不是navplot时，将解析后的数据重组包成navplot输出

| No.  | 名称        | 描述                      | 格式   |
| ---- | ----------- | ------------------------- | ------ |
| 0    | gps_week    | GPS周                     | uint   |
| 1    | gps_sec     | GPS周内秒                 | float  |
| 2    | lat         | 纬度                      | double |
| 3    | lon         | 经度                      | double |
| 4    | alt         | 大地高                    | float  |
| 5    | ve          | 东向速度                  | float  |
| 6    | vn          | 北向速度                  | float  |
| 7    | vu          | 天向速度                  | float  |
| 8    | roll        | 横滚角                    | float  |
| 9    | pitch       | 俯仰角                    | float  |
| 10   | heading     | 航向角（0~360°，正北为0） | float  |
| 11   | postype     | 定位状态                  | uint   |
| 12   | instype     | 组合状态                  | uint   |
| 13   | n_sat       | 使用卫星数                | uint   |
| 14   | gnss_status | 纯卫导状态                | uint   |
| 15   | std_lat     | 纬度标准差                | float  |
| 16   | std_lon     | 经度标准差                | float  |
| 17   | std_alt     | 大地高标准差              | float  |
| 18   | std_ve      | 东向速度标准差            | float  |
| 19   | std_vn      | 北向速度标准差            | float  |
| 20   | std_vu      | 天向速度标准差            | float  |
| 21   | std_roll    | 横滚角标准差              | float  |
| 22   | std_pitch   | 俯仰角标准差              | float  |
| 23   | std_heading | 航向角标准差              | float  |

