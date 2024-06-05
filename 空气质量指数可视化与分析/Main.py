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

@app.route('/qryform')
def qryform():
    return render_template('qryform.html')

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


@app.route('/chartmap3')
def chartmap():
    return render_template('chartmap3.html')

@app.route('/viewmap')
def viewmap():
    return render_template('viewmap.html')

if __name__ == '__main__':
    app.run(debug=True)