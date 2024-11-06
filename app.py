from apscheduler.schedulers.blocking import BlockingScheduler
import database as db
import pandas as pd
import time
import filter as f
from autoEmail import sendEmail

def job_1():
    print("任务1在每天9点15分执行。")

def  check():
	sql = '''
		SELECT 
		ts_code,ts_name
		,sum(shares) as shareholding
		,round(sum(amout)/sum(shares),3) as holding_cost
		FROM mytradingrecord
		group by 1,2
	'''

	myHoldings=db.select(sql )
	myHoldings = pd.DataFrame(myHoldings, columns=['ts_code', 'ts_name','holdings','price'])
	print(myHoldings)

	for index, value in myHoldings.iterrows():
		ts_code,ts_name,holdings,price = value
		code=ts_code[0:6]


		try:
			liveData=f.get_LiveData(code,ts_name)
		except:
			time.sleep(6)
			try:
				liveData=f.get_LiveData(code,ts_name)
			except:
				time.sleep(16)
				liveData=f.get_LiveData(code,ts_name)
		# print(liveData)
		
		# 基于当日行情，判断一下当前状态：
		currentPrice=float(liveData.loc[code,'currentPrice'])
		preClose=float(liveData.loc[code,'preClose'])
		profit_ratio=round((currentPrice-price)*100/price,3)
		increase=round((currentPrice-preClose)*100/preClose,3)
		print(ts_name+'当前价格：'+str(currentPrice)+'收益'+str(profit_ratio)+'涨幅'+str(increase))


		if profit_ratio>10 :
			myHoldings.loc[index,'type']='saleable'
			# 这里的清仓策略待补充 --- 原则上出现回落迹象则果断清仓

		elif profit_ratio>5 :
			# 激进做T,当日上午的涨幅超2%,清仓等待接回.
			myHoldings.loc[index,'type']='overtrading'
		elif profit_ratio >0 :
			# 观测状态 不做任何操作
			myHoldings.loc[index,'type']='peep_1'
		elif profit_ratio>-5 :
			# 观测状态 不做任何操作
			myHoldings.loc[index,'type']='peep_2'

		elif profit_ratio >-10:
			# 保守做T  当日跌幅超2%，一倍买入  逢高卖出
			myHoldings.loc[index,'type']='undertrading'
			if increase <-2 :
				myHoldings.loc[index,'op']='buy'
				sendEmail(ts_name,'buy')
		else :
			myHoldings.loc[index,'type']='tear_up '
		# print('上一次交易价格：'+str(last_deal))
		
		print('=======================================')
		time.sleep(1)

	print(myHoldings)
	# 这里，要把当日的观测列表，保存起来，

def job_2():
    print("任务2在每天14点30分执行。")


auto=(time.strftime("%Y%m%d_%H%M%S"))
print("开始执行任务")
sendEmail('任务开始',auto)


scheduler = BlockingScheduler()
# 第一次执行
scheduler.add_job(check, 'cron', hour='9', minute='35')

# 第二次执行
scheduler.add_job(check, 'cron', hour='10', minute='25')

# 第二次执行
scheduler.add_job(check, 'cron', hour='11', minute='20')


scheduler.start()