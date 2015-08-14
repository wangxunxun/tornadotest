'''
Created on 2015年8月13日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member,DailyReport,WeeklyReport
from ..utils import MakeToken
class inputReportHandler(BaseHandler):
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
            
class viewReportHandler(BaseHandler):
    def get(self,input):
        data = input
        data = data.split('!@')
        memberid = data[0]
        teamid = data[1]
        teamtype = data[2]
        member = self.session.query(Member).filter(Member.id ==memberid).scalar()
        team = self.session.query(Team).filter(Team.id == teamid).scalar()
        print(team)
        if teamtype =='1':
            report = self.session.query(DailyReport).filter(DailyReport.memberid==memberid,DailyReport.teamid==teamid).all()
            self.render('viewdailyreport.html',bodytitle = "查看日报",member = member,team = team,report = report)

        if teamtype =='2':
            report = self.session.query(WeeklyReport).filter(WeeklyReport.memberid==memberid,WeeklyReport.teamid==teamid).all()
            self.render('viewweeklyreport.html',bodytitle = "查看周报",member = member,team = team,report = report)