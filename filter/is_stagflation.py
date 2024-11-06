import time
import pandas as pd
import tushare as ts
from filter import my_token

def  is_stagflation(shareList):
	pro = ts.pro_api(token="52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad")
	ts.set_token('52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad')

	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		
		# 获取数据
		try:
			df = ts.pro_bar(ts_code=ts_code, adj='qfq',factors=['tor', 'vr'])
		except BaseException as e:
			try:
				# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第1次重试.....")
				time.sleep(60)
				df = ts.pro_bar(ts_code=ts_code, adj='qfq',factors=['tor', 'vr'])
				# print("重试成功")
			except Exception as e:
				try:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第2次重试.....")
					time.sleep(120)
					df = ts.pro_bar(ts_code=ts_code, adj='qfq',factors=['tor', 'vr'])
					# print("重试成功")
				except Exception as e:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
					continue

		# 处理
		try:
			stagflation=df.loc[0,'vol']/((df.loc[0,'vol']+df.loc[1,'vol']+df.loc[2,'vol']+df.loc[3,'vol'])/4)-1
			if stagflation <= -0.35 and df.loc[0,'change']>0.5:
				shareList.loc[index,'is_stagflation']='缩量上涨'

			elif stagflation <= -0.35 and df.loc[0,'change']<-0.5:
				shareList.loc[index,'is_stagflation']='缩量下跌'

			elif stagflation >= 0.35 and df.loc[0,'change']>0.5:
				shareList.loc[index,'is_stagflation']='放量上涨'

			elif stagflation >= 0.35 and df.loc[0,'change']<-0.5: 
				shareList.loc[index,'is_stagflation']='放量下跌'

			df.to_excel('./file/pro_bar/bar_'+ts_code+'.xlsx',index=False)
		except Exception as e:
			continue
	return shareList

if __name__ == '__main__':
	print(1)