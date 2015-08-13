import os
currentpath = os.path.dirname(__file__).replace("\\","/")
dbsqlitepath = currentpath+'/data.sqlite'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
host = "localhost"
port = 8000


