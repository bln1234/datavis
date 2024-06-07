import csv
import json

# 打开CSV文件
with open("站点列表.csv", 'r') as csvfile:
    # 创建一个CSV阅读器对象
    csvreader = csv.DictReader(csvfile)
    # 读取CSV文件中的所有行并转换为列表
    data = list(csvreader)
    
# 将数据转换为JSON格式
json_data = json.dumps(data)

# 将JSON数据写入文件
with open("站点列表.json", 'w') as jsonfile:
    jsonfile.write(json_data)

with open("china_sites_20240601.csv", 'r') as csvfile:
    # 创建一个CSV阅读器对象
    csvreader = csv.DictReader(csvfile)
    # 读取CSV文件中的所有行并转换为列表
    data = list(csvreader)

# 将数据转换为JSON格式
json_data = json.dumps(data)

# 将JSON数据写入文件
with open("china_sites_20240601.json", 'w') as jsonfile:
    jsonfile.write(json_data)
