from sqlalchemy import Column, String, create_engine,ForeignKey,Integer,CHAR
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
engine = create_engine('sqlite:///F:/workplace/testtoolbyflask/data.sqlite',echo=False)
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
    name = Column(CHAR(30)) # or Column(String(30))

if __name__ == '__main__':

    user = User(id = 2,name = "3333")
    
    
    query1 = session.query(User).filter(User.id == 2).scalar()
    #session.delete(query1)
    session.commit()
    #print(query1.id)
    query = session.query(User)
    for user in query: # 遍历时查询
        print(user.id)
    
    
    # 关闭session:
    session.close()