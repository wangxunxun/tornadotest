'''
Created on 2015年8月10日

@author: xun
'''
from .baseHandler import BaseHandler
from ..models import User


class LoginHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.render(
            "login.html",
            
            errormessage = ""
        )
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        user = self.session.query(User).filter(User.email ==email).scalar()
        if user:
            if user.verify_password(password):
                self.set_secure_cookie("user", email)
                self.redirect("/teammanage")
            else:
                self.render("login.html", errormessage = "密码错误")
                
        else:
            self.render("login.html", errormessage = "用户不存在")

        
class RegistHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.render("regist.html",errormsg="")

    def post(self):
        email = self.get_argument("email")
        username = self.get_argument("username")
        password = self.get_argument("password")
        password_t = self.get_argument("password_t")
        if password !=password_t:
            self.render("regist.html",errormsg="确认密码和密码不一致")
        elif self.session.query(User).filter(User.email == email).scalar():
            self.render("regist.html", errormsg="该邮箱已注册")
        else:
            self.set_secure_cookie("user", email)
            user=User(name = username,password = password,email =email)
            self.session.add(user)
            self.session.commit()
            self.redirect("/login")

class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect("login")
        
routes = [

    (r"/login",LoginHandler),
    (r"/regist",RegistHandler),
    (r'/logout', LogoutHandler),
        ]
