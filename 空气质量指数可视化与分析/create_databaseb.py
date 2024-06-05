import sqlite3  # 导入SQLite数据库操作模块
import csv  # 导入CSV文件读取模块
# 连接到 SQLite 数据库（如果不存在，则会被创建）
conn = sqlite3.connect('air_quality.db')
# 创建一个游标对象，用于执行 SQL 语句
cursor = conn.cursor()
# 创建一个名为 air_quality 的表格，包含所需的列
cursor.execute('''CREATE TABLE IF NOT EXISTS air_quality
                (id INTEGER PRIMARY KEY AUTOINCREMENT,SITE TEXT,
                TIME TEXT,PM25 INTEGER,PM10 INTEGER,O3 REAL,
                NO2 REAL,SO2 REAL,CO REAL,LONGITUDE REAL,
                LATITUDE REAL)''')
# 读取 CSV 文件并将数据插入到数据库中
with open('aqi_newwww.csv', newline='', encoding='gbk') as csvfile:
    reader = csv.DictReader(csvfile)  # 使用 DictReader 读取 CSV 文件，每行数据被解释为一个字典
    for row in reader:  # 遍历 CSV 文件中的每一行
        # 将数据插入到 air_quality 表中
        cursor.execute('''INSERT INTO air_quality 
                        (SITE, TIME, PM25, PM10, O3, NO2, SO2, CO, LONGITUDE, LATITUDE) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (row['SITE'], row['TIME'], row['PM2.5'], row['PM10'],
                        row['O3'], row['NO2'], row['SO2'], row['CO'], row['经度'], row['纬度']))
# 提交更改并关闭连接
conn.commit()  # 提交对数据库的更改
conn.close()  # 关闭数据库连接
