'''
Created on 2015年8月12日

@author: wangxun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member

class addTeamHandler(BaseHandler):
    def get(self):
        self.render("addteam.html",  bodytitle = "添加小组", error = "")
    def post(self):
        team = self.get_argument("team")
        type = self.get_argument("type")
        if not self.session.query(Team).filter(Team.name ==team).all():
            team1 = Team(name = team,type =type)
            self.session.add(team1)
            self.session.commit()
            self.redirect("/teammanage")
        else:
            self.render("addteam.html",  bodytitle = "添加小组",error = "该小组已添加，不能重复添加")
            
class deleteTeamHandler(BaseHandler):
    def get(self,get):
        id =get
        team = self.session.query(Team).filter(Team.id ==id).scalar()
        joinmembers = team.members.all()
        for member in joinmembers:
            self.session.delete(member)
        self.session.delete(team)
        self.session.commit()
        self.redirect("/teammanage")

class editTeamHandler(BaseHandler):
    def get(self,input):
        team = self.session.query(Team).filter(Team.id == input).scalar()
        self.render("editteam.html",  bodytitle = "编辑小组", team = team,error = "")

    def post(self,input):
        type = self.get_argument("type")
        team = self.session.query(Team).filter(Team.id == input).scalar()
        team.type = type
        self.session.add(team)
        self.session.commit()
        self.redirect("/teammanage")
        
class teamManageHandler(BaseHandler):
    def get(self):
        teams = self.session.query(Team)
        self.render("teammanage.html",  bodytitle = "小组管理", teams = teams)
    def post(self):
        team = self.get_argument("team")
        if not self.session.query(Team).filter(Team.name ==team).all():
            team1 = Team(name = team)
            self.session.add(team1)
            self.session.commit()
            self.render("addteam.html",  bodytitle = "添加小组",error = "添加成功")
        else:
            self.render("addteam.html",  bodytitle = "添加小组",error = "该小组已添加，不能重复添加")