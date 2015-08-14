import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
from app.handlers.userHandler import LoginHandler,RegistHandler,LogoutHandler
from app.handlers.teamHandler import TeamIndexHandler,TeamNoteamHandler
from app.handlers.baseHandler import xmlHandler,NoFoundHandler,SuccessHandler

from app.handlers.MemberHandlers import *
from app.handlers.TeamHandlers import *
from app.handlers.ReportHandlers import *
from app.utils import AutoSendEmail
import settings
from tornado.options import define, options
import threading
from pip._vendor.distlib._backport.tarfile import TUREAD
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self): 
        handlers = [

            (r"/login",LoginHandler),
            (r"/regist",RegistHandler),
            (r'/logout', LogoutHandler),
            (r"/team/noteam", TeamNoteamHandler),
            (r"/", TeamIndexHandler),
            (r"/xml", xmlHandler),
            (r"/addteam", addTeamHandler),
            (r"/addmember", addMemberHandler),
            (r"/teammanage", teamManageHandler),
            (r"/membermanage", memberManageHandler),
            (r"/deleteteam/(.*)", deleteTeamHandler),
            (r"/deletemember/(.*)", deleteMemberHandler),
            (r"/deletejoinedteam/(.*)", deleteJoinedTeamHandler),
            (r"/editteam/(.*)", editTeamHandler),
            (r"/editmember/(.*)", editMemberHandler),
            (r"/inputreport/(.*)", reportHandler),
            (r"/success", SuccessHandler),
            (r"/404", NoFoundHandler),
        ]
        
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "app/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "app/static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            xsrf_cookies=True,
            debug=True,
            login_url="/login",

        )
        
        tornado.web.Application.__init__(self, handlers,**settings)



if __name__ == "__main__":
 
    a = AutoSendEmail.sendmail(settings.mail_host,settings.mail_user,settings.mail_pass,
                               settings.dbsqlitepath,'11:03','11:03')

    t1 =threading.Thread(target=a.dingshiribao)
    t2 =threading.Thread(target=a.dingshizhoubao)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()