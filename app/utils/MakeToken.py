'''
Created on 2015年8月11日

@author: wangxun
'''
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import settings
class Token:
    def generate_newmember_token(self,id,email,name,expiration=3600):
        SECRET_KEY = settings.SECRET_KEY
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'id':id,'email':email,'name':name})
    
    
    def load_token(self,token):
        SECRET_KEY = settings.SECRET_KEY
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False

        return data
    

    def generate_report_token(self,email,name,team, teamtype,expiration=3600):
        SECRET_KEY = settings.SECRET_KEY
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'email':email,'name':name,'team':team,'teamtype':teamtype})
if __name__ == '__main__':  
    token = Token()
    a = token.generate_report_token("email", "name", "team", "teamtype", 3600)
    b = token.load_token(a)
    print(b)