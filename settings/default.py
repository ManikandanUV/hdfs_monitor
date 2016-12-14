import os


EDITS_LOC = '/data/hadoop/hdfs/namenode/current/'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/home/mramakri/', 'hdfs_monitor.db')
ZMQ_PORT = '8742'
API_SERVER_URI = 'http://127.0.0.1:8000/'
print(SQLALCHEMY_DATABASE_URI)
print(ZMQ_PORT)


