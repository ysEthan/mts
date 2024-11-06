import tushare as ts
import time
import pandas as pd
from filter import my_token

pro = ts.pro_api(token="52e9a368958cc817e8e82c8d9aca8304346e48b25ed01f92b649e7ad")

#获取列表
def getShareList(trade_date):
	shareList = pro.daily_basic(ts_code='', trade_date=trade_date, fields='ts_code,pe,pe_ttm,pb,dv_ratio,dv_ttm,volume_ratio,total_mv,close')

	#按以下条件筛选
	# shareList=shareList[shareList['total_mv']>400000]
	# shareList=shareList[shareList['total_mv']<80000000]

	shareList=getBasicInfo(shareList,trade_date)

	shareList.to_excel('./file/shareList123.xlsx',index=False)

	return shareList

# 补齐基础信息
def getBasicInfo(shareList,trade_date):
	#获取基础信息表
	stock_basic = pro.stock_basic(exchange='', trade_date=trade_date, list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
	stock_basic.set_index(['ts_code'],inplace=True)

	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])

		shareList.loc[index,'ts_name']=stock_basic.loc[ts_code,'name']
		shareList.loc[index,'industry']=stock_basic.loc[ts_code,'industry']

	return shareList



# 转换标准格式：
def getStandard(shareList):
	df=pd.DataFrame({},columns=['ts_code','ts_name','industry','total_mv','pb','pe_ttm','roe_2021','or_yoy_2021','roe_2022','or_yoy_2022',\
								'preClose','currentPrice','Increase10','Increase25','high','low','preVolumeRatio','volumeRatio','turnoverRatio'
								,'remark','ma_tendency','volumeChange','up','up2'])


	for index, row in shareList.iterrows():
		df.loc[index,'ts_code']=shareList.loc[index,'ts_code']
		df.loc[index,'ts_name']=shareList.loc[index,'ts_name']

		df.loc[index,'industry']=shareList.loc[index,'industry']
		df.loc[index,'total_mv']=round(shareList.loc[index,'total_mv']/10000,2)
		df.loc[index,'pb']=shareList.loc[index,'pb']
		df.loc[index,'pe_ttm']=shareList.loc[index,'pe_ttm']

		df.loc[index,'roe_2022']=round(shareList.loc[index,'roe_2022'],2)
		df.loc[index,'or_yoy_2022']=round(shareList.loc[index,'or_yoy_2022'],2)
		df.loc[index,'roe_2021']=round(shareList.loc[index,'roe_2021'],2)
		df.loc[index,'or_yoy_2021']=round(shareList.loc[index,'or_yoy_2021'],2)

		df.loc[index,'preClose']=shareList.loc[index,'close']

		df.loc[index,'preVolumeRatio']=round(shareList.loc[index,'volume_ratio'],3)
		df.loc[index,'remark']=""

	# df.set_index(['ts_code'],inplace=True)

	return df




if __name__ == '__main__':
	getShareList('20221014')