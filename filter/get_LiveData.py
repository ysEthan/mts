#coding=utf-8
from lxml import etree
import requests
import re 
import pandas as pd

class b(object):
    def __init__(self,code,name):
        self.code=code
        self.name=name
        self.liveData=pd.DataFrame({},columns=['code','name','volumeRatio'])
    #构造url
    def getUrl(self):
        url="https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?"
        header = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Host": "sp0.baidu.com",
                    "Pragma": "no-cache",
                    "Referer": "https://www.baidu.com/s?wd=%E4%BA%BF%E7%BA%AC%E9%94%82%E8%83%BD",
                    "Sec-Fetch-Dest": "script",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                }
        formdata = {
                    "resource_id": "5353",
                    "group": "quotation_minute_ab",
                    "query": self.code,
                    "code": self.code,
                    "all": "1",
                    "pointType": "string",
                    "dsp": "pc",
                    "requestType": "async",
                    "stockName": self.name,
                    "provideName": "九方智投",
                    "sid": "34099_34112_33607_34107_34134_26350_22160",
                    "cb": "jsonp_1624845303876_39518",
                }
        return self.loadPage(url,header,formdata)

    #爬取页面内容
    def loadPage(self,url,header,formdata):
        response=requests.post(url,headers = header,data=formdata).text
        return self.analyseInfo(response)

    #解析并存储：
    def analyseInfo(self,response):
        pat=re.compile(r'{"open"[\s\S]*?}}',re.I) #模式修正符：忽略大小写
        data=pat.finditer(response)
        for i in data:
            strr=i.group()

            pat_code=re.compile(r'"volumeRatio":"(.*?)",',re.I) 
            volumeRatio=pat_code.findall(strr)[0]

            pat_turnoverRatio=re.compile(r'"turnoverRatio":"(.*?)",',re.I) 
            turnoverRatio=pat_turnoverRatio.findall(strr)[0]

            pat_high=re.compile(r'"high":"(.*?)",',re.I) 
            high=pat_high.findall(strr)[0]

            pat_low=re.compile(r'"low":"(.*?)",',re.I) 
            low=pat_low.findall(strr)[0]

            pat_preClose=re.compile(r'"preClose":"(.*?)",',re.I) 
            preClose=pat_preClose.findall(strr)[0]

            pat_currentPrice=re.compile(r'"currentPrice":"(.*?)"}',re.I) 
            currentPrice=pat_currentPrice.findall(strr)[0]

        # 将数据存入df中
        self.liveData = pd.DataFrame({'code': [self.code],
                           'name': [self.name],
                           'turnoverRatio': [turnoverRatio],
                           'high': [high],
                           'low': [low],
                           'currentPrice': [currentPrice],
                           'preClose': [preClose],
                           'turnoverRatio': [turnoverRatio],
                           'volumeRatio': [volumeRatio]
                            },)   
        return(self.liveData)

def get_LiveData(code,name):
    myDemand=b(code,name)
    liveData=myDemand.getUrl()
    liveData.set_index(['code'],inplace=True)
    return liveData

def get_LiveData_Lst(List):

    for index, row in List.iterrows():
        ts_code=index
        code=ts_code[0:6]
        name=List.loc[index,'ts_name']

        try:
            liveData=get_LiveData(code,name)
        except BaseException as e:
            try:
                print("当前获取",ts_code,"数据出错，错误原因：",e,"\n正在重试.....")
                liveData=get_LiveData(code,name)
                time.sleep(9)
                print("重试成功")
            except Exception as e:
                print("当前获取",ts_code,"数据出错，错误原因：",e,"\n不再重试，跳出循环.....")
                continue
        a=a+1
        if mod(a,31)==30 :
            print(ts_code+'  '+str(a))
            time.sleep(4)


if __name__ == '__main__':
    print(get_LiveData('000887','中鼎股份'))