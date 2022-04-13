from walletServer.utils.dbapi import dbIO
from walletServer.utils.dbconfigs import MySQL

lm = MySQL()
lm.bindServer('localhost', 3306, 'wallet')
lm.login('root', 'allan19950601')

dba = dbIO(lm)