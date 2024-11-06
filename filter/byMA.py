import time
import pandas as pd
import tushare as ts
from filter import my_token

def  filtrateByMa(shareList):
	
	pro = ts.pro_api(token=my_token.get_token())
	ts.set_token(my_token.get_token())

	# shareList=shareList.head(150)
	# print(shareList.head())
	
	# 遍历shareList
	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		
		# 获取数据
		try:
			df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[3,5,10,20,30,60])
		except BaseException as e:
			try:
				print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第1次重试.....")
				time.sleep(60)
				df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[3,5,10,20,30,60])
				# print("重试成功")
			except Exception as e:
				try:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第2次重试.....")
					time.sleep(120)
					df = ts.pro_bar(ts_code=ts_code, adj='qfq',ma=[3,5,10,20,30,60])
					# print("重试成功")
				except Exception as e:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
					continue
		# 处理数据
		try:
			# 长期均线高于短期均线
			ii=0
			shareList.loc[index,'ma_tendency']=0
			while df.loc[ii,'ma30']>df.loc[ii,'ma10'] :
				shareList.loc[index,'ma_tendency']=ii
				ii=ii+1

			# 金叉生成
			if df.loc[1,'ma10']>df.loc[1,'ma5'] and  df.loc[0,'ma10']<df.loc[0,'ma5']:
				shareList.loc[index,'ma_x']=99
			else:	
				shareList.loc[index,'ma_x']=0

			# 25交易日降幅 
			p25=df.loc[25,'close']
			p10=df.loc[10,'close']
			p0=df.loc[0,'close']
			shareList.loc[index,'Increase10']=round(round((p0-p10)/p10,4)*100,2)
			shareList.loc[index,'Increase25']=round(round((p0-p25)/p25,4)*100,2)
			
			if (p0-p25)/p25 <= -0.25 :
				shareList.loc[index,'drop']=999
			else:
				shareList.loc[index,'drop']=0

			# 是否出现滞涨
			stagflation=df.loc[0,'vol']/((df.loc[0,'vol']+df.loc[1,'vol']+df.loc[2,'vol']+df.loc[3,'vol'])/4)-1
			if stagflation <= -0.35 :
				shareList.loc[index,'volumeChange']='缩量'


			if df.loc[1,'ma3']<=df.loc[2,'ma3'] and df.loc[0,'ma3']>df.loc[1,'ma3']:
				shareList.loc[index,'up2']='转折上升'


		except Exception as e:
			continue

	#按以下条件筛选
	# shareList=shareList[shareList['Increase25']<-10]
	shareList=shareList.sort_values(by="ma_tendency", ascending=False)
	return shareList


if __name__ == '__main__':
	print(1)



	