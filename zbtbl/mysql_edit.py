import pymysql
import random

# 数据库连接配置
config = {
    'user': 'inklue',
    'password': '20231017ink',
    "host": "47.93.189.31",
    "port": 3306,
    'database': 'course_design',
    'charset': 'utf8mb4'  # pymysql 通常需要指定字符集
}

try:
    # 连接到数据库
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    # 查询表中所有行
    select_query = "SELECT id, crowd_degree FROM map_feature"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for row in rows:
        id_value = row[0]
        crowd_degree = row[1]

        if crowd_degree is not None:
            # 生成随机字符串
            random_str = '/'.join([str(random.choice([0, 1, 2])) for _ in range(3)])
            # 生成更新语句
            update_query = "UPDATE map_feature SET crowd_degree = %s WHERE id = %s"
            cursor.execute(update_query, (random_str, id_value))

    # 提交更改
    connection.commit()
    print("更新操作已成功提交")

except pymysql.Error as err:
    print(f"发生错误: {err}")
finally:
    # 关闭游标和连接
    if cursor:
        cursor.close()
    if connection:
        connection.close()