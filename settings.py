import os
currentpath = os.path.dirname(__file__).replace("\\","/")
dbsqlitepath = currentpath+'/data.sqlite'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'



#自动发送邮件配置信息
host = "localhost"
port = 8000
mail_host="smtp.163.com"  #设置服务器
mail_user="beyondsoftbugzilla@163.com"    #用户名
mail_pass="wangxun2"   #口令
dailyreporttime = '16:21'
weeklyreportday = 'Friday'
weeklyreporttime = '16:21'
