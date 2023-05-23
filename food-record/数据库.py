from pymysql import Connection

#创建MySQL数据库链接
conn=Connection(
    host='localhost',
    port=3306,
    user='root',
    password='1592@klull'
)

#游标对象
cursor=conn.cursor()
#选择数据库
conn.select_db("test")
#执行sql
cursor.execute("create table test_pymysql(id int);")

conn.close()

