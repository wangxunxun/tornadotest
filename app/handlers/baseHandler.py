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
    def get_current_user(self):
        return self.get_secure_cookie("user")


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)
    
 
        
class RecommendedHandler(BaseHandler):
    @tornado.web.authenticated
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