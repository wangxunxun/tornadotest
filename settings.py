import os
currentpath = os.path.dirname(__file__).replace("\\","/")
dbsqlitepath = 'sqlite:///'+currentpath+'/data.sqlite'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


