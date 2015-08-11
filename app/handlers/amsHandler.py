'''
Created on 2015年8月11日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member
import tornado.web

class addTeamHandler(BaseHandler):
    def get(self):
        self.render("addteam.html",  bodytitle = "添加小组", error = "")
    def post(self):
        team = self.get_argument("team")
        if team:
            team1 = Team(name = team)
            self.session.add(team1)
            self.session.commit()
            self.render("addteam.html",  bodytitle = "添加小组",error = "添加成功")
        else:
            self.render("addteam.html",  bodytitle = "添加小组",error = "请输入小组名")

class addMemberEmailHandler(BaseHandler):
    def get(self):
        self.render("addmember_email.html",  bodytitle = "添加成员", error = "")
    def post(self):
        email = self.get_argument("email")
        name = self.get_argument("name")
        if email:
            member1 = Member(email = email,name = name)

            self.session.add(member1)
            self.session.commit()
            self.render("addmember_email.html",  bodytitle = "添加成员",error = "添加成功")
                            
        else:
            self.render("addmember_email.html",  bodytitle = "添加成员",error = "请输入邮箱")
            
class editMemberTeamHandler(BaseHandler):
    
    def get(self):
        teams = self.session.query(Team).all()
        self.render("addmember_team.html",  bodytitle = "添加小组", error = "",teams = teams)
    def post(self):
        teams = self.session.query(Team).all()
        chooseteam = self.get_argument("teams")
        print(len(chooseteam))
        print(chooseteam)
        if chooseteam:


            self.render("addmember_team.html",  bodytitle = "添加小组",error = "添加成功",teams = teams)
                            
        else:
            self.render("addmember_team.html",  bodytitle = "添加小组",error = "请输入邮箱",teams = teams)
    