'''
Created on 2015年8月13日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member,Report
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
        email = data.get('email')
        name = data.get('name')
        team = data.get('team')
        teamtype = data.get('teamtype')
        if teamtype == 1:
            today = self.get_argument("todaysummary")
            tomorrow = self.get_argument("tomorrowsummary")
            issue = self.get_argument("issue")
            dailyreport = Report(email = email,name = name,team = team,teamtype = teamtype,\
                                      today = today,tomorrow = tomorrow,issue = issue)
            self.session.add(dailyreport)
            self.session.commit()
            self.redirect('/teammanage')
        else:
            currentweek = self.get_argument("currentweek")
            nextweek = self.get_argument("nextweek")
            issue = self.get_argument("issue")
            weeklyreport = Report(email = email,name = name,team = team,teamtype = teamtype,\
                                      currentweek = currentweek,nextweek = nextweek,issue = issue)
            self.session.add(weeklyreport)
            self.session.commit()
            self.redirect('/teammanage')
            