import pymysql
# ---------连接--------------
connect = pymysql.connect(host='rm-wz9fm83i33i818q0v0o.mysql.rds.aliyuncs.com',   # 本地数据库
                          user='root',
                          password='MJ7zTcy8$kzQJx5',
                          db='myshare',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cursor = connect.cursor()

def db_select(sql):
	cursor.execute(sql)
	data=cursor.fetchall()
	print('成功返回', cursor.rowcount, '条数据')
	return data 

# 仅返回结果条数 
def db_select2(sql):
	cursor.execute(sql)
	data=cursor.fetchall()
	print('成功返回', cursor.rowcount, '条数据')
	return cursor.rowcount


def db_execute(sql):
	cursor.execute(sql)
	connect.commit()



	# # 关闭连接
	# cursor.close()
	# connect.close()
