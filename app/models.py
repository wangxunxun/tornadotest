from sqlalchemy import Column, String, create_engine,ForeignKey,Integer,CHAR
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import settings



BaseModel = declarative_base()
engine = create_engine(settings.dbsqlitepath,echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)
# 创建新User对象:
class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30)) 
    email = Column(CHAR(),unique = True)
    password_hash = Column(CHAR(128))


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def changeemail(self,email):
        self.email = email
        session.add(self)
        session.commit()

if __name__ == '__main__':
    drop_db()
    init_db()
    email = "59853844@qq.com"
#    user = User(name = "3333",email = "598353844@qq.com")
#    a=session.query(User).filter(User.email ==  "59853844@qq.com").scalar()
#    user = session.query(User).filter(User.id=='3').scalar()
#    print(user)
#    user.changeemail("59853844@qq.com")
#    user.email = "59853844@qq.com"
#    session.add(user)
#    session.commit()



#    User = User()
#    print(User.test("444"))
#    session.add(user)
    session.commit()
#    query1 = session.query(User).filter(User.id == 2).scalar()
    #session.delete(query1)
#    session.commit()
    #print(query1.id)
#    query = session.query(User)
#    for user in query: # 遍历时查询
#        print(user.id)
    
    

    session.close()