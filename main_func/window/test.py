import yaml

project_config = {
        'data' : []
}

# 新建十个数据集
for i in range(10):
    project_config['data'].append({
        'data_path': i.__str__(),
        'dev_name': i.__str__(),
        'data_format': i.__str__(),
        'data_frq': i.__str__(),
        'is_bchmk': i.__str__()
        })

# 将其以yaml格式输出
print(yaml.dump(project_config))
