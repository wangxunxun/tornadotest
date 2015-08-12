'''
Created on 2015年8月11日

@author: wangxun
'''
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from settings import SECRET_KEY
class Token:
    def generate_newmember_token(self,id,email,name,expiration=3600):
        SECRET_KEY1 = SECRET_KEY
        s = Serializer(SECRET_KEY1, expiration)
        return s.dumps({'id':id,'email':email,'name':name})
    
    
    def newmember_token(self,token):
        SECRET_KEY1 = SECRET_KEY
        s = Serializer(SECRET_KEY1)
        try:
            data = s.loads(token)
        except:
            return False

        return data
    

    def generate_report_token(self,email,name,team,expiration=3600):
        SECRET_KEY = SECRET_KEY
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'email':email,'name':name,'team':team})
    
    def edit_report(self,token):
        SECRET_KEY = SECRET_KEY
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        result = {}
        email = data.get('email')
        name = data.get('name')
        team = data.get('team')
        result.setdefault('email',email)
        result.setdefault('name',name)
        result.setdefault('team',team)
        return result