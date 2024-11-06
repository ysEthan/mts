import database as db
import time
import pandas as pd
from autoEmail import sendEmail

def  import_tradingRecord():
	# 刷新数据，把Excel表里面的数据全部导入到 mysql 中
	fileName='./file/00_myHoldings.xlsx'	
	myShareList=pd.read_excel(fileName,sheet_name='tradingRecord',header=0,index_col=0)

	for index, value in myShareList.iterrows():
		ts_code,deal_type,deal_time,ts_name,price,shares,amout,trading_fee,stamp_tax = value
		sql="INSERT INTO myTradingRecord "
		sql=sql+ "(id,ts_code,deal_type,deal_time,ts_name,price,shares,amout,trading_fee,stamp_tax)"
		sql=sql+"VALUES ("+str(index)+""
		sql=sql+",'"+   str(ts_code) +"'"
		sql=sql+",'"+   str(deal_type) +"'"
		sql=sql+",'"+   str(deal_time) +"'"
		sql=sql+",'"+   str(ts_name) +"'"
		sql=sql+",'"+   str(price) +"'"
		sql=sql+",'"+   str(shares) +"'"
		sql=sql+",'"+   str(amout) +"'"
		sql=sql+",'"+   str(trading_fee) +"'"
		sql=sql+",'"+   str(stamp_tax) +"'"
		sql=sql+") "

		sql=sql+"ON DUPLICATE KEY UPDATE "
		sql=sql+" ts_code ='"+str(ts_code)+"'" 
		sql=sql+" ,shares ='"+str(shares)+"'" 
		sql=sql+" ,price ='"+str(price)+"'" 
		sql=sql+" ,trading_fee ='"+str(trading_fee)+"'" 
		sql=sql+" ,stamp_tax ='"+str(stamp_tax)+"'" 
		# print(sql)
		db.insert(sql)



print("Start")
while 1==1:
	import_tradingRecord()	

	# s_left=86400-(int(time.strftime("%H"))*3600+int(time.strftime("%M")) *60+int(time.strftime("%S")))+3600*14.5
	# print(time.strftime("%Y%m%d_%H%M%S"))
	# print(s_left/3600)
	# print('==============================================================================')
	# time.sleep(s_left)
	time.sleep(3600*12)
