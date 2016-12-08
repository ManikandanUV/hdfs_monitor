import os


EDITS_LOC = '/data/hadoop/hdfs/namenode/current/'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/home/mramakri/', 'hdfs_monitor.db')
ZMQ_PORT = '8742'
print(SQLALCHEMY_DATABASE_URI)
print(ZMQ_PORT)

