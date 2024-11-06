import pymysql
# ---------连接--------------
connect = pymysql.connect(host='rm-wz9fm83i33i818q0v0o.mysql.rds.aliyuncs.com',   # 本地数据库
                          user='root',
                          password='MJ7zTcy8$kzQJx5',
                          db='myshare',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cursor = connect.cursor()

def insert(sql):
	cursor.execute(sql)
	connect.commit()
