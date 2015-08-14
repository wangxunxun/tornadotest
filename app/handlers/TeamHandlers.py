'''
Created on 2015年8月12日

@author: wangxun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member
import tornado.web
class addTeamHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("addteam.html",  bodytitle = "添加小组", error = "")
    @tornado.web.authenticated
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
    @tornado.web.authenticated
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
    @tornado.web.authenticated
    def get(self,input):
        team = self.session.query(Team).filter(Team.id == input).scalar()
        self.render("editteam.html",  bodytitle = "编辑小组", team = team,error = "")
    @tornado.web.authenticated
    def post(self,input):
        teamname = self.get_argument('teamname')
        teamtype = self.get_argument("type")

            
        team = self.session.query(Team).filter(Team.id == input).scalar()
        if teamname == team.name:
            team.type = teamtype
            team.name = teamname
            teammembers = self.session.query(Team_member).filter(Team_member.teamid == input).all()
            for teammember in teammembers:
                teammember.teamname = teamname
                self.session.add(teammember)
            self.session.add(team)
            self.session.commit()
            self.redirect("/teammanage")

        elif self.session.query(Team).filter(Team.name == teamname).scalar():
            self.render("editteam.html",  bodytitle = "编辑小组", team = team,error = "该小组已存在")
        else:
            team.type = teamtype
            team.name = teamname
            teammembers = self.session.query(Team_member).filter(Team_member.teamid == input).all()
            for teammember in teammembers:
                teammember.teamname = teamname
                self.session.add(teammember)
            self.session.add(team)
            self.session.commit()
            self.redirect("/teammanage")
                
        
class teamManageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        teams = self.session.query(Team)
        self.render("teammanage.html",  bodytitle = "小组管理", teams = teams)
    @tornado.web.authenticated
    def post(self):
        team = self.get_argument("team")
        if not self.session.query(Team).filter(Team.name ==team).all():
            team1 = Team(name = team)
            self.session.add(team1)
            self.session.commit()
            self.render("addteam.html",  bodytitle = "添加小组",error = "添加成功")
        else:
            self.render("addteam.html",  bodytitle = "添加小组",error = "该小组已添加，不能重复添加")