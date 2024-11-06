import time
import pandas as pd
import tushare as ts
from filter import my_token
 


def  filtrateByIncrease(shareList):
	pro = ts.pro_api(token=my_token.get_token())
	ts.set_token(my_token.get_token())

	# shareList=shareList.head(50)
	# print(shareList.head())

	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		
		try:
			df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[5,10,20,30,60])
		except BaseException as e:
			try:
				# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第1次重试.....")
				time.sleep(60)
				df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[5,10,20,30,60])
				# print("重试成功")
			except Exception as e:
				try:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第2次重试.....")
					time.sleep(120)
					df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[5,10,20,30,60])
					# print("重试成功")
				except Exception as e:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
					continue
		try:
			p30=df.loc[29,'close']
			p0=df.loc[0,'close']

			shareList.loc[index,'p30']=p30
			shareList.loc[index,'p0']=p0
			shareList.loc[index,'Increase30']=(p0-p30)/p30

			if (p0-p30)/p30 <= -0.25 :
				shareList.loc[index,'drop']=999
			elif (p0-p30)/p30 >= 0.25 :
				shareList.loc[index,'drop']=888
			else:
				shareList.loc[index,'drop']=0

		except Exception as e:
			continue
	return shareList


if __name__ == '__main__':
	print(1)