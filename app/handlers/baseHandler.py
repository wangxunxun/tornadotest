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
    
class MainpageHandler(BaseHandler):
    def get(self):
        self.render("mainpage.html")
        
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
    
 
