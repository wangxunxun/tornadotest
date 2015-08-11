'''
Created on 2015年8月11日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member
import tornado.web
from ..utils import token 

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
            if not self.session.query(Member).filter(Member.email==email).scalar():
                member1 = Member(email = email,name = name)
                self.session.add(member1)
                self.session.commit()
                user = self.session.query(Member).filter(Member.email==email).scalar()  
                print(user.id)          
                self.redirect("/editmemberteam/"+str(user.id))
            else:
                self.render("addmember_email.html",  bodytitle = "添加成员",error = "该邮箱已注册")
                            
        else:
            self.render("addmember_email.html",  bodytitle = "添加成员",error = "请输入邮箱")
            
class editMemberTeamHandler(BaseHandler):
    
    def get(self,input):

        userid = int(input)
        if self.session.query(Member).filter(Member.id ==userid).scalar():
            teams = self.session.query(Team).all()
            self.render("addmember_team.html",  bodytitle = "添加小组", error = "",teams = teams)
        else:
            self.redirect("/404")
    def post(self,input):

        teams = self.session.query(Team).all()
        userid = int(input)
        body = str(self.request.body)
        print(self.request.body)
        print(body.split('&'))
        items = body.split('&')
        i = 1
        a = []
        while i<len(items):
            print(items[i])
            if i!=len(items)-1:
                a.append(items[i][6:len(items[i])])
            else:
                a.append(items[i][6:len(items[i])-1])
            i = i+1
        print(a)

        chooseteam1 = self.get_argument('teams')
        chooseteam2 = self.get_argument('teams')
        
        print(chooseteam1)
        print(chooseteam2)


        if chooseteam1:
            tm = Team_member(teamid =1,memberid = userid)
            self.session.add(tm)
            self.session.commit()


            self.render("addmember_team.html",  bodytitle = "添加小组",error = "添加成功",teams = teams)
                            
        else:
            self.render("addmember_team.html",  bodytitle = "添加小组",error = "请选择小组",teams = teams)
    