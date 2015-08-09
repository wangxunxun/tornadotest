'''
Created on 2015年8月8日

@author: wangxun
'''
import tornado.web
from .. import models
from ..models import User



class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = models.session

    def on_finish(self):
        self.session.close()


class MainHandler(BaseHandler):
    def get(self):
        self.render(
            "index.html",
            
        )
class LoginHandler(BaseHandler):
    def get(self):
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
                self.redirect("/")
            else:
                self.render("login.html", errormessage = "密码错误")
                
        else:
            self.render("login.html", errormessage = "用户不存在")

        
class RegistHandler(BaseHandler):
    def get(self):
#        self.set_secure_cookie("user", "")
        self.render("regist.html",
                     regist=False, errormsg="")

    def post(self):
        email = self.get_argument("email")
        username = self.get_argument("username")
        password = self.get_argument("password")
        password_t = self.get_argument("password_t")
        if password !=password_t:
            self.render("regist.html", regist=False, errormsg="确认密码和密码不一致")
        elif self.session.query(User).filter(User.email == email).scalar():
            self.render("regist.html", regist=False, errormsg="该邮箱已注册")
        else:
            user=User(name = username,password = password,email =email)
            self.session.add(user)
            self.session.commit()
            self.render("regist.html",regist=True, username=username, errormsg="")

                

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)
    
class RecommendedHandler(BaseHandler):
    def get(self):
        self.render(
            "recommended.html",
            
            books=[
                {
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"/static/images/collective_intelligence.gif",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                }
            ]
        )