'''
Created on 2015年8月12日

@author: wangxun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member
import tornado.web
from app.handlers.ReportHandlers import routes

class deleteMemberHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,get):
        id =get
        member = self.session.query(Member).filter(Member.id ==id).scalar()
        jointeams = member.teams.all()
        for team in jointeams:
            self.session.delete(team)
        self.session.delete(member)
        self.session.commit()
        self.redirect("/membermanage")

class deleteJoinedTeamHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,get):
        data =get.split("!@")
        memberid =data[0]
        teamid = data[1]
        teammember = self.session.query(Team_member).filter(Team_member.teamid == teamid,Team_member.memberid==memberid).scalar()
        self.session.delete(teammember)
        self.session.commit()
        self.redirect("/editmember/"+memberid)
            
class memberManageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        members = self.session.query(Member)
        membersdata = []        
        for member in members:
            memberinfo = {}
            memberinfo.setdefault('id',member.id)
            memberinfo.setdefault('email',member.email)
            memberinfo.setdefault('name',member.name)
            teams = []
            for team in member.teams:
                data = self.session.query(Team).filter(Team.id == team.teamid).scalar()
                teaminfo = {}
                teaminfo.setdefault('id',data.id)
                teaminfo.setdefault('type',data.type)
                teaminfo.setdefault('name',data.name)
                teams.append(teaminfo)
            memberinfo.setdefault('teams',teams)
            membersdata.append(memberinfo)      
        self.render("membermanage.html",  bodytitle = "人员管理", members = membersdata)


            
class addMemberHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        allteams = self.session.query(Team).all()

        self.render("addmember.html", bodytitle = "添加成员", error = "",teams = allteams)

    @tornado.web.authenticated
    def post(self):
        email = self.get_argument("email")
        name = self.get_argument("name")
        allteams = self.session.query(Team).all()
        chooseteams =self.get_arguments("teams") 
        teamsid = []
        for i in chooseteams:
            que = self.session.query(Team).filter(Team.name ==i).scalar()
            teamsid.append(que.id)
        if allteams:
            if not self.session.query(Member).filter(Member.email==email).scalar():
                member1 = Member(email = email,name = name)
                self.session.add(member1)
                self.session.commit()
                id = self.session.query(Member).filter(Member.email == email).scalar().id
                if teamsid:
                    i = 0
                    while i<len(teamsid):
                        tm = Team_member(teamid =teamsid[i],memberid = id)
                        self.session.add(tm)
                        i = i+1
                        
    
                    self.session.commit()
                    self.redirect("/membermanage")
                                                
                else:
                    self.render("addmember.html",  bodytitle = "添加成员",error = "请选择小组",teams = allteams)
            else:
                self.render("addmember.html",  bodytitle = "添加成员",error = "该邮箱已注册",teams = allteams)
        else:
            self.render("addmember.html",  bodytitle = "添加成员",error = "请先创建小组",teams = allteams)


class editMemberHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        id = input
        member = self.session.query(Member).filter(Member.id == id).scalar()
        memberinfo = {}
        memberinfo.setdefault('email',member.email)
        memberinfo.setdefault('name',member.name)
        memberinfo.setdefault('id',member.id)
        teams = []
        for team in member.teams:
            teaminfo = {}
            data = self.session.query(Team).filter(Team.id == team.teamid).scalar()
            teaminfo.setdefault('id',data.id)
            teaminfo.setdefault('type',data.type)
            teaminfo.setdefault('name',data.name)
            teams.append(teaminfo)
        memberinfo.setdefault('teams',teams)

        allteams = self.session.query(Team).all()

        savedteams = self.session.query(Member).filter(Member.id == id).scalar().teams.all()
        savedteamsid = []
        for t in savedteams:
            savedteamsid.append(t.teamid)             
        nosavedteam = []
        for i in allteams:
            if i.id not in savedteamsid:
                nosavedteam.append(i)

        self.render("editmember.html",  member = memberinfo,bodytitle = "编辑成员", error = "",teams = nosavedteam)

    @tornado.web.authenticated
    def post(self,input):
        newname = self.get_argument("username")                  
        chooseteams =self.get_arguments("teams") 
        id = input
        member = self.session.query(Member).filter(Member.id == id).scalar()
        teamsid = []
        for i in chooseteams:
            que = self.session.query(Team).filter(Team.name ==i).scalar()
            teamsid.append(que.id)
        i = 0
        while i<len(teamsid):
            tm = Team_member(teamid =teamsid[i],memberid = id)
            self.session.add(tm)

            i = i+1
        member.name =newname
        self.session.add(member)
        self.session.commit() 
        self.redirect("/membermanage")


routes = [


    (r"/addmember", addMemberHandler),

    (r"/membermanage", memberManageHandler),

    (r"/deletemember/(.*)", deleteMemberHandler),
    (r"/deletejoinedteam/(.*)", deleteJoinedTeamHandler),

    (r"/editmember/(.*)", editMemberHandler),

        ]