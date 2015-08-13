'''
Created on 2015年8月8日

@author: wangxun
'''
import tornado.web
from .. import models
from ..models import User
import os
from ..utils import ExportXmlByBeyondsoft
from win32api import ShellExecute
from win32con import SW_SHOWNORMAL 


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = models.session

    def on_finish(self):
        self.session.close()
    def get_current_user(self):
        return self.get_secure_cookie("user")
    
class NoFoundHandler(BaseHandler):
    def get(self):
        self.render("404.html")
        
class SuccessHandler(BaseHandler):
    def get(self):
        self.render("success.html")

class xmlHandler(BaseHandler):
    def get(self):
        self.render("xml.html",errormsg = "",isexcel = False,sheets = "")
        
    def post(self):
        excelname = self.get_argument("excel")
        sheetname = self.get_argument("sheet")
        output = self.get_argument("output")
        xmlname = self.get_argument("xmlname")
        sheets = ExportXmlByBeyondsoft.exceloperate(excelname).getSheetNames()
        if os.path.exists(excelname):
            try:     
                sheets = ExportXmlByBeyondsoft.exceloperate(excelname).getSheetNames()  
                self.render("xml.html",errormsg = "文件名不存在",isexcel = True,sheets = sheets) 
            except:
                self.render("xml.html",errormsg = "文件名不存在",isexcel = False,sheets = "")

            
            if sheetname in sheets:
                if os.path.exists(output):
                    
                    xmlfile = output.replace('/',"\\")+"\\"+xmlname+".xml"
                    aa =ExportXmlByBeyondsoft.changetoxml(excelname,sheetname,output,xmlname)  
                    try:                      
                        aa.run()
                        ShellExecute(0,"open",xmlfile,"","",SW_SHOWNORMAL)
                        self.render("xml.html",errormsg = "成功转换",isexcel = False,sheets = "")
                        self.redirect("/xml")

                    except:
                        self.render("xml.html",errormsg = "请参照用例模板设计用例",isexcel = False,sheets = "")

                    
                else:
                    os.mkdir(output)
                    xmlfile = output.replace('/',"\\")+"\\"+xmlname+".xml"
                    aa =ExportXmlByBeyondsoft.changetoxml(excelname,sheetname,output,xmlname)
                    try:                      
                        aa.run()
                        ShellExecute(0,"open",xmlfile,"","",SW_SHOWNORMAL)
                        self.render("xml.html",errormsg = "成功转换",isexcel = False,sheets = "")
                        self.redirect("/xml")

                    except:
                        self.render("xml.html",errormsg = "请参照用例模板设计用例",isexcel = False,sheets = "")
            else:

                self.render("xml.html",errormsg = "该表格不存在",isexcel = False,sheets = "")
                
        else:
            self.render("xml.html",errormsg = "该用例文件不攒在",isexcel = True,sheets = sheets)


        
        
        
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