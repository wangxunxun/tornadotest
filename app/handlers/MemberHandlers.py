'''
Created on 2015年8月12日

@author: wangxun
'''
from .baseHandler import BaseHandler
from ..models import User,Team,Member,Team_member
import tornado.web
from ..utils import MakeToken

class deleteMemberHandler(BaseHandler):
    def get(self,get):
        id =get
        member = self.session.query(Member).filter(Member.id ==id).scalar()
        self.session.delete(member)
        self.session.commit()
        self.redirect("/membermanage")


            
class memberManageHandler(BaseHandler):
    def get(self):
        members = self.session.query(Member)
        
        self.render("membermanage.html",  bodytitle = "人员管理", members = members)
    def post(self):
        team = self.get_argument("team")
        if not self.session.query(Team).filter(Team.name ==team).all():
            team1 = Team(name = team)
            self.session.add(team1)
            self.session.commit()
            self.render("addteam.html",  bodytitle = "添加小组",error = "添加成功")
        else:
            self.render("addteam.html",  bodytitle = "添加小组",error = "该小组已添加，不能重复添加")

class addMemberEmailHandler(BaseHandler):
    
    def get(self):
        self.render("addmember_email.html",  bodytitle = "添加成员", error = "")
    def post(self):
        token = MakeToken.Token()
        email = self.get_argument("email")
        name = self.get_argument("name")

        

        if not self.session.query(Member).filter(Member.email==email).scalar():
            member1 = Member(email = email,name = name)
            self.session.add(member1)
            self.session.commit()
            user = self.session.query(Member).filter(Member.email==email).scalar()   
            newtoken = str(token.generate_newmember_token(user.id,email, name))
            newtoken = newtoken[2:len(newtoken)-1]       
            self.redirect("/addmemberteam/"+newtoken)
        else:
            self.render("addmember_email.html",  bodytitle = "添加成员",error = "该邮箱已注册")
                            

            
class addMemberTeamHandler(BaseHandler):
    
    def get(self,input):
        token = MakeToken.Token()
        data = token.newmember_token(input)        
        email = data.get("email")
        name = data.get("name")
        id = data.get('id')
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
              
        if self.session.query(Member).filter(Member.email ==email).scalar():
            self.render("addmember_team.html", email = email,name = name,
                        bodytitle = "添加小组", error = "",teams = nosavedteam)
        else:
            self.redirect("/404")
   
    def post(self,input):
        token = MakeToken.Token()
        data = token.newmember_token(input)        
        email = data.get("email")
        name = data.get("name")
        id = data.get('id')
        allteams = self.session.query(Team).all()
        savedteams = self.session.query(Member).filter(Member.id == id).scalar().teams.all()
        savedteamsid = []
        for t in savedteams:
            savedteamsid.append(t.teamid)             
        nosavedteam = []
        for i in allteams:
            if i.id not in savedteamsid:
                nosavedteam.append(i)
        
        
                       
        chooseteams =self.get_arguments("teams")        
        i = 1
        teamsid = []
        for i in chooseteams:
            que = self.session.query(Team).filter(Team.name ==i).scalar()
            teamsid.append(que.id)

        if teamsid:
            i = 0
            while i<len(teamsid):
                tm = Team_member(teamid =teamsid[i],teamname = chooseteams[i],memberid = id,
                                 memberemail = email)
                self.session.add(tm)
                self.session.commit()
                i = i+1
            self.redirect("/membermanage")
                                        
        else:
            self.render("addmember_team.html",  bodytitle = "添加小组",email = email,
                        name = name,error = "请选择小组",teams = nosavedteam)

class editMemberHandler(BaseHandler):
    
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
              
        if self.session.query(Member).filter(Member.email ==email).scalar():
            self.render("editmember.html",  savedteams = savedteams,email = email,name = name,
                        bodytitle = "添加小组", error = "",teams = nosavedteam)
        else:
            self.redirect("/404")
   
    def post(self,input):
        newname = self.get_argument("username")                  
        chooseteams =self.get_arguments("teams") 
        id = input
        member = self.session.query(Member).filter(Member.id == id).scalar()
        email = member.email
        name = member.name
        print(name)
        print(newname)
        
#        
        


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
