import csv
import mysql.connector

def connect_mysql(host, user, password, database):
    connection = mysql.connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )
    return connection

def read_csv(filename):
    rows = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # skip header
        for row in reader:
            rows.append(row)
    return rows

def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        # row: [weather_id, mars_date, temp, storm]
        mars_date = row[1]
        temp = float(row[2])
        storm = int(row[3])
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        cursor.execute(query, (mars_date, temp, storm))
    connection.commit()
    cursor.close()

def fetch_summary(connection):
    cursor = connection.cursor()
    query = (
        'SELECT COUNT(*), AVG(temp), MAX(temp), MIN(temp), SUM(storm) '
        'FROM mars_weather'
    )
    cursor.execute(query)
    summary = cursor.fetchone()
    cursor.close()
    return summary

def print_summary(summary):
    print('총 데이터 수:', summary[0])
    print('평균 온도:', round(summary[1], 2))
    print('최고 온도:', summary[2])
    print('최저 온도:', summary[3])
    print('폭풍 발생 합계:', summary[4])

def main():
    # MySQL 접속 정보
    host = 'localhost'
    user = 'root'
    password = 'aj072200'
    database = 'mars'

    # 1. MySQL 연결
    connection = connect_mysql(host, user, password, database)

    # 2. CSV 읽기
    filename = 'task12/mars_weathers_data.CSV'
    data = read_csv(filename)
    print('CSV 데이터 일부 미리보기:')
    for row in data[:5]:
        print(row)

    # 3. 데이터 INSERT
    insert_data(connection, data)
    print('데이터가 성공적으로 삽입되었습니다.')

    # 4. 요약 정보 출력
    summary = fetch_summary(connection)
    print_summary(summary)

    connection.close()

if __name__ == '__main__':
    main()
