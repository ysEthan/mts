import tushare as ts
import time
from filter import my_token



def  get_cal():
	pro = ts.pro_api(token=my_token.get_token())
	nowDate=(time.strftime("%Y%m%d"))
	cal = pro.trade_cal(exchange='', start_date='20231001', end_date=nowDate)
	return cal

def  is_open():
	pro = ts.pro_api(token=my_token.get_token())
	nowDate=(time.strftime("%Y%m%d"))
	cal = pro.trade_cal(exchange='', start_date=nowDate, end_date=nowDate)

	return cal.loc[0,'is_open']

def  today():
	pro = ts.pro_api(token=my_token.get_token())
	nowDate=(time.strftime("%Y%m%d"))
	cal = pro.trade_cal(exchange='', start_date=nowDate, end_date=nowDate)
	return cal.loc[0,'cal_date']

def  pretrade_date():
	pro = ts.pro_api(token=my_token.get_token())
	nowDate=(time.strftime("%Y%m%d"))
	cal = pro.trade_cal(exchange='', start_date=nowDate, end_date=nowDate)
	return cal.loc[0,'pretrade_date']

if __name__ == '__main__':
	if is_open() ==0:
		print(get_cal())

	else:
		print("今天不是交易日")
