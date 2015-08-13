'''
Created on 2015年8月3日

@author: xun
'''

import sqlite3
import os
import smtplib  
from email.mime.text import MIMEText  
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from time import sleep
import datetime
import time, os, sched 
import random,threading,time
from queue import Queue
from settings import SECRET_KEY,host,port,dbsqlitepath
import settings

    


class oprsql:
    def __init__(self,sql):
        self.sql = sql
        self.coon = sqlite3.connect(self.sql)
        self.cur=self.coon.cursor()


    def getmembers(self):                

        self.cur.execute('select * from member')
        result=self.cur.fetchall()
        i = 0
        members = []
        while i<len(result):
            memberid = result[i][0]
            email = result[i][1]
            name = result[i][2]
            self.cur.execute('select teamname from teammember where memberemail = "%s"'%email)
            teamnames = self.cur.fetchall()
            self.cur.execute('select teamid from teammember where memberemail = "%s"'%email)
            teamids = self.cur.fetchall()
            print(teamids)
            if len(teamids) ==1:
                member = {}
                self.cur.execute('select type from team where id ="%s"'%teamids[0][0])
                teamtype = self.cur.fetchone()[0]
                member.setdefault("memberid",memberid)
                member.setdefault("email",email)
                member.setdefault("name",name)
                member.setdefault('teamid',teamids[0][0])   
                member.setdefault('teamname',teamnames[0][0]) 
                member.setdefault('teamtype',teamtype)             
                members.append(member)
            else:
                j = 0
                
                while j<len(teamids):
                    member ={}
                    self.cur.execute('select type from team where id ="%s"'%teamids[j][0])
                    teamtype = self.cur.fetchone()[0]
                    member.setdefault("memberid",memberid)
                    member.setdefault("email",email)
                    member.setdefault("name",name)
                    member.setdefault('teamid',teamids[j][0])  
                    member.setdefault('teamname',teamnames[0][0])  
                    member.setdefault('teamtype',teamtype)             
                    members.append(member)     
                    j=j+1               
            i =i +1
        return members
    
class oprtoken:

    def generate_report_token(self,id,email,name,teamid,team, teamtype,expiration=3600):
        SECRET_KEY = settings.SECRET_KEY
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'memberid':id,'email':email,'name':name,'teamid':teamid,'teamname':team,'teamtype':teamtype})
    
    def edit_report(self,token):
        SECRET_KEY = settings.SECRET_KEY
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        return data
    
    
class sendmail:
    
    def __init__(self,host,user,pas,sqlite):
        self.host = host
        self.user = user
        self.pas = pas
        self.sql =sqlite
        self.schedule = sched.scheduler(time.time, time.sleep) 

        

    
    def send_mail(self,to_list,sub,content):
        me="beyondsoft.ams"+" <"+self.user+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
        msg['Subject'] = sub    #设置主题
        msg['From'] = me  
        msg['To'] = ";".join(to_list)  
        try:  
            s = smtplib.SMTP()  
            s.connect(self.host)  #连接smtp服务器
            s.login(self.user,self.pas)  #登陆服务器
            s.sendmail(me, to_list, msg.as_string())  #发送邮件
            s.close()  
            return True  
        except Exception as e:
            print(e)
            return False  
        
    def autosend(self):
        members = oprsql(self.sql)
        members = members.getmembers()
        i = 0
        while i<len(members):
            memberid = members[i].get('memberid')
            email = members[i].get('email')
            teamid = members[i].get('teamid')
            name = members[i].get('name')
            teamtype = members[i].get('teamtype')
            teamname = members[i].get('teamname')
            print(teamtype)
            oprt = oprtoken()
            token = oprt.generate_report_token(memberid,email, name, teamid,teamname,teamtype, 3600)
            token = str(token)
            token = token[2:len(token)-1]
            host = settings.host
            port = settings.port
            reporturl ="http://"+host+":"+str(port)+"/inputreport/"+token    
            daycontent = "<h5>Hello "+name+",</h5>\
        <p>您今天的日报链接已经创建，请于今天18:30 前填写提交.</p>\
        <p>本日报隶属于<strong>"+teamname+"</strong>小组</p>\
        <p>链接地址: <a href="+reporturl+">click here</a></p>\
        谢谢"
            weekcontent = "<h5>Hello "+name+",</h5>\
        <p>您今天的周报链接已经创建，请于今天18:30 前填写提交.</p>\
        <p>本日报隶属于<strong>"+teamname+"</strong>小组</p>\
        <p>链接地址: <a href="+reporturl+">click here</a></p>\
        谢谢"
            mailto_list=[email] 
            if teamtype==1:

                if self.send_mail(mailto_list,"QA Team小组-日报创建提醒 ",daycontent):  
                    print("发送成功")  
                else:  
                    print("发送失败")  
            else:
                if self.send_mail(mailto_list,"QA Team小组-日报创建提醒 ",weekcontent):  
                    print("发送成功")  
                else:  
                    print("发送失败")  
                

                
            i =i+1        
    def dingshi(self):
        while True:
            if datetime.datetime.now().strftime('%H:%M:%S') == "13:51:00":
                self.autosend()
                sleep(1)

    def perform_command(self,inc):
        self.schedule.enter(inc, 0, self.perform_command, (inc,))  
        self.autosend()
                
    def timming_exe(self,inc = 60): 
        # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
        self.schedule.enter(inc, 0, self.perform_command, (inc,)) 
        # 持续运行，直到计划时间队列变成空为止 
        self.schedule.run()         
        
class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self,name=t_name)
        self.data=queue
    def run(self):
        while True:
            if datetime.datetime.now().strftime('%H:%M:%S') == "15:09:00":
                self.data.put(1)
                print(self.data)
                sleep(1)
       
class Consumer(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self,name=t_name)
        self.data=queue
    def run(self):
        while 1:
            try:
                val_even = self.data.get(1,86400) #get(self, block=True, timeout=None) ,1就是阻塞等待,5是超时5秒
                if val_even == 1:
                    mail_host="smtp.163.com"  #设置服务器
                    mail_user="beyondsoftbugzilla@163.com"    #用户名
                    mail_pass="wangxun2"   #口令 
                    sql = 'C:/Users/xun/workspace/testtoolbyflask/data.sqlite'
                    a = sendmail(mail_host,mail_user,mail_pass,sql)
                    a.autosend()
            except:   #等待输入，超过5秒 就报异常
                print ("%s: %s finished!" %(time.ctime(),self.getName()))
                break        


if __name__ == '__main__':  
    
#    SECRET_KEY = Config().SECRET_KEY
#    print(SECRET_KEY)
    mail_host="smtp.163.com"  #设置服务器
    mail_user="beyondsoftbugzilla@163.com"    #用户名
    mail_pass="wangxun2"   #口令 
    a = sendmail(mail_host,mail_user,mail_pass,dbsqlitepath)
#    print(dbsqlitepath)
    b =oprsql(dbsqlitepath)
    a.autosend()

    print(b.getmembers())
#    t =threading.Thread(target=a.dingshi)
#    t.start()
#    a.autosend()
#    a.timming_exe(120)
#    a.dingshi()
#    queue = Queue()
#    producer = Producer('Pro.', queue)
#    consumer = Consumer('Con_even.', queue)
#    producer.setDaemon(True)
#    consumer.setDaemon(True)
#    print(111)
#    producer.start()
#     consumer.start()
    

