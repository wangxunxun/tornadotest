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
    def __repr__(self):
        return '<User %r>' % self.name
        
        
class Member(BaseModel):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    email = Column(CHAR(),unique = True)
    name = Column(CHAR()) 
    teams = relationship('Team_member',backref='member', lazy='dynamic')
    

    
    def __repr__(self):
        return '<Member %r>' % self.name

class Team(BaseModel):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR()) 
    members = relationship('Team_member',backref='team', lazy='dynamic')
    


    def __repr__(self):
        return '<Team %r>' % self.name
    
class Team_member(BaseModel):
    __tablename__ = 'teammember'
    id = Column(Integer, primary_key=True)
    teamid = Column(Integer, ForeignKey('team.id'))
    teamname = Column(CHAR()) 
    memberid = Column(Integer, ForeignKey('member.id'))
    memberemail = Column(CHAR()) 
    


    def __repr__(self):
        return '<Team_member %r>' % self.teamid

if __name__ == '__main__':
#    drop_db()
#    init_db()
    email = "59853844@qq.com"
    m = session.query(Member).filter(Member.email =="59853844@qq.com").scalar()
    t = session.query(Team).all()
    for i in t:
        print(i.name)
    print(m.email)
    print(m.teams.all())
#    team1 = Team(name = "kaifa")
#    member1 = Member(email = "5985384433@qq.com",name = "test")
#    session.add(team1,member1)
#    session.add(member1)
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