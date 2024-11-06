# coding=utf-8
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


from tkinter import messagebox

def sendEmail(subject,content):
	sender="huangzhenshen@126.com" #发送方
	pwd="CGFXMRLGSJSYXOLF"#授权码  
	recipient="757819951@qq.com"

	msgRoot = MIMEMultipart('related')
	msgRoot['From'] = sender
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgRoot['To'] =  recipient 
	msgRoot['Subject'] = subject
	msgAlternative.attach(MIMEText(content, 'html', 'utf-8'))

	    #发送邮件
	try:
	    ss=smtplib.SMTP_SSL("smtp.126.com",465)
	    ss.login(sender,pwd)
	    ss.sendmail(sender,recipient,msgRoot.as_string()) #发送


	except Exception as e:
	    print(e)


if __name__ == '__main__':
	subject="st"
	content="123"
	sendEmail(subject,content)