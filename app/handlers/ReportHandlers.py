'''
Created on 2015年8月13日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member,DailyReport,WeeklyReport
from ..utils import MakeToken
class reportHandler(BaseHandler):
    def get(self,input):
        token = MakeToken.Token()
        data = token.load_token(input)
        teamtype = data.get('teamtype')
        if teamtype == 1:
            self.render('dailyreport.html',bodytitle = "日报填写",data = data)
        else:
            self.render('weeklyreport.html',bodytitle = "周报填写",data = data)
            
    def post(self,input):

        token = MakeToken.Token()
        data = token.load_token(input)

        memberid = data.get('memberid')
        email = data.get('email')
        name = data.get('name')
        teamid = data.get('teamid')
        team = data.get('teamname')
        teamtype = data.get('teamtype')
        if teamtype == 1:
            today = self.get_argument("todaysummary")
            tomorrow = self.get_argument("tomorrowsummary")
            issue = self.get_argument("issue")
            dailyreport = DailyReport(memberid = memberid,teamid = teamid,today = today,tomorrow = tomorrow,issue = issue)
            self.session.add(dailyreport)
            self.session.commit()
            self.redirect('/success')
        else:
            currentweek = self.get_argument("currentweek")
            nextweek = self.get_argument("nextweek")
            issue = self.get_argument("issue")
            weeklyreport = WeeklyReport(memberid = memberid,teamid = teamid,currentweek = currentweek,nextweek = nextweek,issue = issue)
            self.session.add(weeklyreport)
            self.session.commit()
            self.redirect('/success')
            