'''
Created on 2015年8月12日

@author: wangxun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member
import tornado.web

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
        print(get)
        data =get.split("!@")
        print(data)
        memberid =data[0]
        teamid = data[1]
        print(memberid)
        print(teamid)
        teammember = self.session.query(Team_member).filter(Team_member.teamid == teamid,Team_member.memberid==memberid).scalar()
        print(teammember.id)
        self.session.delete(teammember)
        self.session.commit()

        self.redirect("/editmember/"+memberid)
            
class memberManageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        members = self.session.query(Member)
        dailyteams = self.session.query(Team).filter(Team.type ==1).all()
        weeklyteams = self.session.query(Team).filter(Team.type ==2).all()

        dailyteamid =[]
        weeklyteamid =[]
        for team in dailyteams:
                dailyteamid.append(team.id)
        for team in weeklyteams:
            weeklyteamid.append(team.id)

                
                
                
        
        self.render("membermanage.html",  bodytitle = "人员管理", members = members,dailyteamid = dailyteamid,
                    weeklyteamid = weeklyteamid)


            
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
                        tm = Team_member(teamid =teamsid[i],teamname = chooseteams[i],memberid = id,
                                         memberemail = email)
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
        email = member.email
        name = member.name

        allteams = self.session.query(Team).all()
        print(self.session.query(Member).filter(Member.id == id).scalar())
        savedteams = self.session.query(Member).filter(Member.id == id).scalar().teams.all()
        savedteamsid = []
        for t in savedteams:
            savedteamsid.append(t.teamid)             
        nosavedteam = []
        for i in allteams:
            if i.id not in savedteamsid:
                nosavedteam.append(i)
                
        dailyteams = self.session.query(Team).filter(Team.type ==1).all()
        weeklyteams = self.session.query(Team).filter(Team.type ==2).all()

        dailyteamid =[]
        weeklyteamid =[]
        for team in dailyteams:
                dailyteamid.append(team.id)
        for team in weeklyteams:
            weeklyteamid.append(team.id)
              
        if self.session.query(Member).filter(Member.email ==email).scalar():
            self.render("editmember.html",  savedteams = savedteams,member = member,
                        bodytitle = "编辑成员", error = "",teams = nosavedteam,dailyteamid = dailyteamid,
                        weeklyteamid = weeklyteamid)
        else:
            self.redirect("/404")
    @tornado.web.authenticated
    def post(self,input):
        newname = self.get_argument("username")                  
        chooseteams =self.get_arguments("teams") 
        id = input
        member = self.session.query(Member).filter(Member.id == id).scalar()
        email = member.email
        allteams = self.session.query(Team).all()
        savedteams = self.session.query(Member).filter(Member.id == id).scalar().teams.all()
        savedteamsid = []

        for t in savedteams:
            savedteamsid.append(t.teamid)             
        nosavedteam = []
        for i in allteams:
            if i.id not in savedteamsid:
                nosavedteam.append(i)       
        i = 1
        teamsid = []
        for i in chooseteams:
            que = self.session.query(Team).filter(Team.name ==i).scalar()
            teamsid.append(que.id)

        i = 0
        while i<len(teamsid):
            tm = Team_member(teamid =teamsid[i],teamname = chooseteams[i],memberid = id,
                             memberemail = email)
            self.session.add(tm)

            i = i+1
        member.name =newname
        self.session.add(member)
        self.session.commit() 
        self.redirect("/membermanage")
