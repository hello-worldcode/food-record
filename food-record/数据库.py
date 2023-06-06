import mysql.connector


# 填写数据库连接参数
config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': 'test',
    'raise_on_warnings': True
}

cnx=mysql.connector.connect(**config)

# 创建一个游标对象
cursor = cnx.cursor()

# 执行 SQL 查询
query = "SELECT * FROM test1_pymysql"
cursor.execute(query)

# 获取查询结果
result = cursor.fetchall()

# 打印查询结果
for row in result:
    print(row)

# 关闭游标和数据库连接
cursor.close()
cnx.close()


