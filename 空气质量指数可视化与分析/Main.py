from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# SQLite数据库文件路径
DATABASE = 'air_quality.db'

def connect_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/AQI.html')
def qryform():
    return render_template('AQI.html')

@app.route('/get_stations', methods=['GET', 'POST'])

def get_stations():
    try:
        # 连接到 SQLite 数据库
        conn = connect_db()
        if conn is None:
            return jsonify({'error': '无法连接到数据库'})

        cur = conn.cursor()

        # 从数据库检索站点数据
        cur.execute("SELECT SITE, LATITUDE, LONGITUDE, PM25, PM10, O3, SO2, CO, NO2 FROM air_quality")
        station_data = cur.fetchall()

        # 过滤唯一坐标
        unique_coordinates = set()
        unique_station_data = []

        for row in station_data:
            latitude = row[1]
            longitude = row[2]

            # 检查坐标是否唯一
            if (latitude, longitude) not in unique_coordinates:
                unique_coordinates.add((latitude, longitude))
                unique_station_data.append(row)


        # 关闭数据库连接
        cur.close()
        conn.close()

        # 将数据转换为字典列表
        stations = [{'SITE': row[0], 'PM2_5': row[3], 'PM10': row[4], 'O3':row[5], 'SO2': row[7], 'NO2': row[6], 'CO': row[8], 'LONGITUDE': row[2], 'LATITUDE': row[1]} for row in unique_station_data]

        for row in stations:
            print('Row:', row)

        # 返回经过过滤后的站点数据
        return jsonify(stations)

    except Exception as e:
        print(f"发生错误：{e}")
        return jsonify({'error': '发生意外错误'})


@app.route('/get_station_data/<string:station_name>')
def get_station_data(station_name):
    try:
        # 连接到 SQLite 数据库
        conn = connect_db()
        if conn is None:
            return jsonify({'error': '无法连接到数据库'})

        cur = conn.cursor()

        # 从数据库检索特定站点的历史数据
        cur.execute(f"SELECT TIME, PM25, PM10, O3, SO2, CO, NO2 FROM air_quality WHERE SITE = ? ORDER BY TIME", (station_name,))
        station_data = cur.fetchall()

        # 关闭数据库连接
        cur.close()
        conn.close()

        # 将数据转换为字典列表
        historical_data = [{'TIME': row[0], 'PM2_5': row[1], 'PM10': row[2], 'O3': row[3], 'SO2': row[4], 'CO': row[5], 'NO2': row[6]} for row in station_data]

        # 返回特定站点的历史数据
        return jsonify({'station_name': station_name, 'historical_data': historical_data})

    except Exception as e:
        print(f"发生错误：{e}")
        return jsonify({'error': '发生意外错误'})


@app.route('/chartmap3.html')
def chartmap():
    return render_template('chartmap3.html')

@app.route('/viewmap.html')
def viewmap():
    return render_template('viewmap.html')



def calculate_average(values):
    valid_values = [float(v) for v in values if isinstance(v, (int, float, str)) and v is not None and v != '']
    if valid_values:
        return sum(valid_values) / len(valid_values)
    return None

@app.route('/air_quality', methods=['GET'])
def get_air_quality():
    conn = sqlite3.connect('AQI_data.db')
    cursor = conn.cursor()

    # 这里可以为每个字段创建别名，以便于后续访问
    query = """
    SELECT 
        StationCode AS station_code,
        StationName AS station_name,
        CITY AS city,
        Longitude AS longitude,
        Latitude AS latitude,
        (0, 'AQI') AS aqi_0,
        (0, 'PM2_5_24h') AS pm2_5_24h,
        (0, 'PM10_24h') AS pm10_24h,
        (0, 'SO2_24h') AS so2_24h,
        (0, 'NO2_24h') AS no2_24h,
        (0, 'O3_24h') AS o3_24h,
        (0, 'CO_24h') AS co_24h
    FROM aqi_data
    """  # 替换为你的实际表名
    cursor.execute(query)
    rows = cursor.fetchall()

    # 获取列名
    columns = [column[0] for column in cursor.description]

    # 构建JSON响应
    data = []
    for row in rows:
        station_data = dict(zip(columns, row))

        # 计算AQI的日均值
        aqi_values = [station_data.get('aqi_0')]
        station_data['AQI'] = calculate_average(aqi_values)

        # 直接从数据库中获取其他指标的日均值
        station_data['PM2_5'] = float(station_data.get('pm2_5_24h', 0))
        station_data['PM10'] = float(station_data.get('pm10_24h', 0))
        station_data['SO2'] = float(station_data.get('so2_24h', 0))
        station_data['NO2'] = float(station_data.get('no2_24h', 0))
        station_data['O3'] = float(station_data.get('o3_24h', 0))
        station_data['CO'] = float(station_data.get('co_24h', 0))

        data.append(station_data)

    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)