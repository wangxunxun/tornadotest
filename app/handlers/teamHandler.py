'''
Created on 2015年8月10日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User
import tornado.web

class TeamIndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie("user")
        user = self.session.query(User).filter(User.email == email).scalar()
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        team = None
        if team:
            teamid = str(team['_id'])
            self.redirect('/team/detail/' + teamid)
        else:
            self.redirect('/team/noteam')
            
class TeamNoteamHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie("user")
        user = self.session.query(User).filter(User.email == email).scalar()
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        self.render("team_noteam.html", username=username)

    @tornado.web.authenticated
    def post(self, teamID):
        pass

    @tornado.web.authenticated
    def put(self, teamID):
        pass

    @tornado.web.authenticated
    def delete(self, teamID):
        pass
