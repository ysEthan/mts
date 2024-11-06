import tushare as ts
import time
import pandas as pd




#获取列表
def get_pivot(shareList):


	pivot =	{
	  "total": 0,
	  "rise": 0,
	  "ohter": 0
	}

	for index, row in shareList.iterrows():
		ts_code=str(shareList.loc[index,'ts_code'])
		pivot["total"]=pivot["total"]+1
		if shareList.loc[index,'up2']=='上涨趋势' :
			pivot["rise"]=pivot["rise"]+1

	percent=str(round(pivot["rise"]*100/pivot["total"],2))+'%'

	strr='<tr><td>'+str(pivot["total"])+'</td><td>'+str(pivot["rise"])+'</td><td>'+str(percent)+'</td></tr>'

	content=strr
	subject='Operation Tips'
	content='<table border="1" style="font-size:16px;">   <tr>   <th>Total</th><th>rise</th><th>comment</th>    </tr>'+content+   '</table>'

	shareList=shareList.head(25)


	content2='<p>List:</p>'

	content3=''
	print(shareList)
	for index, row in shareList.iterrows():
		strr='<tr><td>'+str(index)+'</td><td>'+str(shareList.loc[index,'ma_tendency'])+'</td><td>'+str(shareList.loc[index,'Increase25'])+'</td><td>'+str(shareList.loc[index,'up2'])+'</td></tr>'
		content3=content3+strr

	content3='<table border="1" style="font-size:16px;"><tr>  <th>ts_name</th>  <th>ma_tendency</th>  <th>Increase25</th> <th>up2</th>  </tr>'+content3+'</table>'


	return content+content2+content3

if __name__ == '__main__':
	getShareList('20221014')



