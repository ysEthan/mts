from lxml import etree
import requests
import re 
import time
import pandas as pd
import smtplib
import xlwt
from functools import partial
import tushare as ts

import numpy as np

pro = ts.pro_api(token="6b6eab34ea42bcdb84161e8993950a73e82f756d2d054682dfe05582")
ts.set_token('6b6eab34ea42bcdb84161e8993950a73e82f756d2d054682dfe05582')

def  filtrateByRoe(shareList):
	print("  获取ROE数据_2022.....")
	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		try:
			data_2022 = pro.fina_indicator(ts_code=ts_code,period='20221231',fields='ts_code,end_date,roe_waa,or_yoy')
		except BaseException as e:
			try:
				# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第1次重试.....")
				time.sleep(60)
				data_2022 = pro.fina_indicator(ts_code=ts_code,period='20221231',fields='ts_code,end_date,roe_waa,or_yoy')
				# print("重试成功")
			except Exception as e:
				try:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第2次重试.....")
					time.sleep(120)
					data_2022 = pro.fina_indicator(ts_code=ts_code,period='20221231',fields='ts_code,end_date,roe_waa,or_yoy')
					# print("重试成功")
				except Exception as e:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
					continue
		try:	
			shareList.loc[index,'roe_2022']=data_2022.loc[0][2]
			shareList.loc[index,'or_yoy_2022']=data_2022.loc[0][3]
		except Exception as e:
			continue
	shareList=shareList[shareList['roe_2022']>15]
	shareList=shareList[shareList['or_yoy_2022']>5]




	print("  获取ROE数据_2021.....")
	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		try:
			data_2021 = pro.fina_indicator(ts_code=ts_code,period='20211231',fields='ts_code,end_date,roe_waa,or_yoy')
		except BaseException as e:
			try:
				# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第1次重试.....")
				time.sleep(60)
				data_2021 = pro.fina_indicator(ts_code=ts_code,period='20211231',fields='ts_code,end_date,roe_waa,or_yoy')
				# print("重试成功")
			except Exception as e:
				try:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在进行第2次重试.....")
					time.sleep(120)
					data_2021 = pro.fina_indicator(ts_code=ts_code,period='20211231',fields='ts_code,end_date,roe_waa,or_yoy')
					# print("重试成功")
				except Exception as e:
					# print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
					continue
		try:	
			shareList.loc[index,'roe_2021']=data_2021.loc[0][2]
			shareList.loc[index,'or_yoy_2021']=data_2021.loc[0][3]
		except Exception as e:
			continue
	shareList=shareList[shareList['roe_2021']>15]
	shareList=shareList[shareList['or_yoy_2021']>5]
	return shareList

if __name__ == '__main__':
	filtrateByRoe(shareList)