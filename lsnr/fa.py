'''
Created on 2018年7月16日

@author: shixi
'''
from comm import Conf
from comm import mysqlUtil
from comm import LLog
from comm import sqlConnPool
  
log = LLog.Logger("fa").getLogger()


def initDB():
#     db = mysqlUtil.dbUtil(Conf.dbHost, Conf.dbUser, Conf.dbPass)
#     db.selectDb(Conf.databaseName)
#     return db
    global dbpool
    sqlConnPool.dbpool = sqlConnPool.SqlConnPool(Conf.dbHost, Conf.dbUser, Conf.dbPass, Conf.databaseName, "utf8", Conf.poolSetSize)
    sqlConnPool.dbpool.start()
    print(sqlConnPool.dbpool)
    print(sqlConnPool.dbpool.connList.qsize())
    db = sqlConnPool.SqlExec()
    return db
    
class Lsnrctl(object):
    
    def start(self):
        log.debug("Lsnrctl-enter-runs")
        self.db=initDB()
        log.debug("Lsnrctl-enter-runs-end")
        

    
if __name__ == '__main__':
    lsn = Lsnrctl()
    lsn.start()
    print(lsn.db)
