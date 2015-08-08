import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
from app.handlers.baseHandler import MainHandler,BookModule,RecommendedHandler

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),(r"/recommended",RecommendedHandler)
        ]
        
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "app/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "app/static"),
            debug=True,
            ui_modules={'Book': BookModule}
        )
        
        tornado.web.Application.__init__(self, handlers,**settings)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()