import tushare as ts
import time
from filter import my_token

def  letTheBulletsFly(n):
	for i in range(1,n):
		# print(my_token.get_token())
		pro = ts.pro_api(token=my_token.get_token())
		df = pro.daily()
		# print(df)
		# print("======================================================================================================")
		time.sleep(18)


