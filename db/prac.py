import mysql.connector
from mysql.connector import Error

def create_connection(host_name, port, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port=port,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("데이터베이스에 성공적으로 연결되었습니다.")
    except Error as e:
        print(f"에러 발생: '{e}'")
    return connection

def list_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("테이블 목록:")
    for table in tables:
        print(table[0])

def fetch_table_data(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    # 컬럼 이름 가져오기
    column_names = [i[0] for i in cursor.description]
    print(f"\n테이블 '{table_name}'의 데이터:")
    print("\t".join(column_names))
    for row in rows:
        print("\t".join(str(item) for item in row))

def main():
    host = "10.231.238.32"
    port = 31044
    user = "root"
    password = "minkyo1111"
    database = "fortune_bot"

    connection = create_connection(host, port, user, password, database)

    if connection is not None:
        list_tables(connection)
        
        # 예시로 첫 번째 테이블의 데이터를 가져옵니다.
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        if tables:
            first_table = tables[0][0]
            fetch_table_data(connection, first_table)
        else:
            print("데이터베이스에 테이블이 없습니다.")
        
        connection.close()
        print("데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
