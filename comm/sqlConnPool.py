'''
Created on 2018/7/24

@author: shixi
'''
import Conf
import pymysql
from  LLog import Logger
import time
from enum import Enum, unique
import threading
import queue
current_milli_time = lambda: int(round(time.time() * 1000))

log = Logger("SqlConnPoll").getLogger()
dbpool = None
 
# 
# class SharedCounter:
#     '''
#     A counter object that can be shared by multiple threads.
#     '''
#     _lock = threading.RLock()
# 
#     def __init__(self, initial_value=0):
#         self._value = initial_value
# 
#     def incr(self, delta=1):
#         '''
#         Increment the counter with locking
#         '''
#         with SharedCounter._lock:
#             self._value += delta
# 
#     def decr(self, delta=1):
#         '''
#         Decrement the counter with locking
#         '''
#         with SharedCounter._lock:
#              self.incr(-delta)
# 
# 
# lock = SharedCounter()


@unique
class ConnStat(Enum):
    OK = 1
    ERROR = 2
    

class ConnPack():
    lock = threading.Lock()

    def connect(self):
        ConnPack.lock.acquire()
        try:  
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.password)  
            self.conn.set_charset(self.charset)  
            # thread No Safe
#             self.cur = self.conn.cursor()
            self.conn.select_db(self.dbName)
        except pymysql.Error as e:  
            log.error("Mysql Conn Error %d: %s" % (e.args[0], e.args[1]))
            raise  e
        finally: 
            ConnPack.lock.release()    

    def cursor(self):
        if self.conn:
            return self.conn.cursor()

    def close(self):
        try:
            if self.conn:
                return self.conn.close()
        except Exception as e: 
            log.error("ConnPack-close,%s" % (e))

    def commit(self):
        if self.conn:
            return self.conn.commit()

    def setStat(self, connStat):
        self.status = connStat

    def __init__(self, host, user, password, dbName, charset="utf8"):
        self.host = host  
        self.user = user  
        self.password = password  
        self.charset = charset
        self.dbName = dbName
        # init
        self.ids = -1
        self.startTime = current_milli_time()
        try:
#             self.conn = self.connect() ERROR
            self.connect()
            self.status = ConnStat.OK
        except Exception as e: 
            log.error("Mysql Conn init  Error %s", e)
            self.status = ConnStat.ERROR
            self.conn = None
        finally:
            log.error("ConnPack()")


class SqlConnPool(object):
   
    def __init__(self, host, user, password, dbName, charset="utf8", setSize=10):
        self.host = host  
        self.user = user  
        self.password = password  
        self.charset = charset
        self.dbName = dbName
        self.setSize = setSize
        self.connList = queue.Queue(setSize)
        self.errorConnList = queue.Queue(setSize)
        self.inits()
        self.stopFlag = True

    def reBoot(self):
        self.inits()
        
    def hb(self):
        while self.stopFlag:
            log.debug("hb-size:%d,%d,%s" % (self.connList.qsize(), self.errorConnList.qsize(), self.stopFlag))
            if self.errorConnList.qsize() > 0:
                oldConn = self.errorConnList.get()
                oldConn.close()
                conn = ConnPack(self.host, self.user , self.password , self.dbName, self.charset)
                conn.ids = conn.startTime
                self.connList.put(conn, block=False)
                log.debug("hb-put-%s" % (conn))
            time.sleep(1)
            log.debug("hb-size-end:%d,%s" % (self.connList.qsize(), self.stopFlag))
        log.debug("hb-stop:%d" % (self.connList.qsize()))

    def start(self):
        log.debug("pool-thread-start")
        t = threading.Thread(target=self.hb, daemon=True)
        self.thread = t 
        # ERROR
#         self.thread.daemon=True
        self.thread.start()
        
    def stop(self):
#         //TODO
#         self.thread._stop()
        self.stopFlag = False
       
    def inits(self):
        if Conf._isDebugs == True:
            for i in range(5):
                conn = ConnPack(self.host, self.user , self.password , self.dbName, self.charset)
                print("pool inits %s" % (conn))
                conn.ids = conn.startTime
                self.connList.put(conn)
            for j in range(5):
                conn = ConnPack(self.host, self.user , self.password , self.dbName, self.charset)
                print("pool inits %s" % (conn))
                conn.ids = conn.startTime
                self.errorConnList.put(conn)
        else:
            for k in range(self.setSize):
                conn = ConnPack(self.host, self.user , self.password , self.dbName, self.charset)
                print("pool inits %s" % (conn))
                conn.ids = conn.startTime
                self.connList.put(conn)

    def get(self):
        return  self.connList.get()

    def take(self):
        return  self.connList.get_nowait()

    def put(self, conn):
        try:
            self.connList.put(conn)
        except Exception as e:
            try:
                conn.close()
            except Exception as e2:
                log.error("SqlConnPool-put-conn-close-Error%s" % (e))
            log.error("SqlConnPool-put-conn-Error%s" % (e))
            pass

    def putError(self, conn):
        try:
            self.errorConnList.put(conn)
        except Exception as e:
            conn.close()
            log.error("SqlConnPool-put-conn%s" % (e))
            pass
        
    def qsize(self):
        return self.connList.qsize()

    def errorQsize(self):
        return self.errorConnList.qsize()


class SqlExec(object):
    
#     def query(self, sql):  
#         try:  
#             n = dbpool.get().execute(sql)  
#             return n  
#         except pymysql.Error as e:  
#             log.error("Mysql Error:%s\nSQL:%s" % (e, sql))
#         finally:
#               
  
    def execs(self, sql):  
        try:  
#             print ("execs-SqlExec-execs-dbpool:",dbpool)
            start = current_milli_time()
            global dbpool 
            conn = dbpool.get()
#             print("execs",conn)
            cur = conn.cursor()
            n = cur.execute(sql)
#             time.sleep(3)
            cur.close()
            conn.commit()
            dbpool.put(conn)
            return n 
        except pymysql.Error as e:  
            try:
                cur.close()  
                conn.close()
            except Exception as e1:
                log.error("Mysql Error:%s--%s--SQL:%s" % (conn, e1, sql)) 
                pass
            log.error("Mysql Error:%s--%s--SQL:%s" % (conn, e, sql)) 
            dbpool.putError(conn)
            raise e 
        finally:
#             log.debug("mysql execs %d---%d---%s" % ((current_milli_time() - start), conn.ids, sql))
            pass
        
        try:  
            print ("SqlExec-execs-dbpool:", dbpool)
            start = current_milli_time()
            conn = dbpool.get()
            cur = conn.cursor()
            n = cur.execute(sql)  
            conn.commit()  
            cur.close()
            dbpool.put(conn)
            return n  
        except pymysql.Error as e:  
            cur.close()  
            conn.close()
            log.error("Mysql Error:%d--%s--SQL:%s" % (conn.ids, e, sql)) 
            raise e 
        finally:
            log.debug("mysql execs %d---%d---%s" % ((current_milli_time() - start), conn.ids, sql))
   
    def queryAll(self, sql):  
        try:  
#             print ("queryAll-SqlExec-execs-dbpool:",dbpool)
            start = current_milli_time()
            global dbpool 
            conn = dbpool.get()
#             print("queryAll",conn)
            cur = conn.cursor()
            n = cur.execute(sql)
            result = cur.fetchall()  
            desc = cur.description  
            d = []  
            for inv in result:  
                _d = {}  
                for i in range(0, len(inv)):  
                    _d[desc[i][0]] = str(inv[i])  
                d.append(_d)  
#             time.sleep(3)
            cur.close()
            dbpool.put(conn)
            return d  
        except pymysql.Error as e:  
            try:
                cur.close()  
                conn.close()
            except Exception as e1:
                log.error("Mysql Error:%s--%s--SQL:%s" % (conn, e1, sql)) 
                pass
            log.error("Mysql Error:%s--%s--SQL:%s" % (conn, e, sql)) 
            dbpool.putError(conn)
            raise e 
        finally:
#             log.debug("mysql execs %d---%d---%s" % ((current_milli_time() - start), conn.ids, sql))
            pass
  
    def insert(self, p_table_name, p_data):  
        
        for key in p_data:  
            p_data[key] = "'" + str(p_data[key]) + "'"  
        key = ','.join(p_data.keys())  
        value = ','.join(p_data.values())  
        real_sql = "INSERT INTO " + p_table_name + " (" + key + ") VALUES (" + value + ")"  
#         self.query("set names 'utf8'")  
        return self.execs(real_sql)  
   
      
def runTest():
    i = 0
#     while True:
    for k in range(20000):
        try:
            db = SqlExec()
            i = i + 1
            if i % 10000 == 0:
                print("runTest %d" % (i))
                db.queryAll("select * from test3")
            db.queryAll("select * from test2")
        except pymysql.Error as e:  
            print(e)


def  testExec():
    start = current_milli_time()
    global dbpool
    dbpool = SqlConnPool(Conf.dbHost, Conf.dbUser, Conf.dbPass, Conf.databaseName, "utf8", Conf.poolSetSize)
    dbpool.start()
    print(dbpool)
    print(dbpool.connList.qsize())
    db = SqlExec()
    db.execs("delete from test2")
    db.execs('insert into test2 values("3","sxm")')
    print(db.queryAll("select * from test2"))
    dbpool.stop()
    for i in range(dbpool.qsize()):
        print("stop-print", i, dbpool.take())
    print("__main__STOP_", current_milli_time() - start)


def testMThreadQueryAll():
    global dbpool
    dbpool = SqlConnPool(Conf.dbHost, Conf.dbUser, Conf.dbPass, Conf.databaseName, "utf8", Conf.poolSetSize)
    dbpool.start()
    print(dbpool)
    print(dbpool.connList.qsize())
    tList = set([])
    start = current_milli_time()
#     //Test Thread Num
    for i in range(15):
        print("__main__LOOP", i)
#         print(db.queryAll("select * from test2"))
        tt = threading.Thread(target=runTest)
        tt.start()        
        tList.add(tt)
        print("__main__LOOP_end", i)
    for t in tList:
        t.join()
         
    print(dbpool.qsize(), dbpool.errorQsize())
    dbpool.stop()
    for i in range(dbpool.qsize()):
        print("stop-print", i, dbpool.take())
    print("__main__STOP_", current_milli_time() - start)

     
if __name__ == '__main__':
  testMThreadQueryAll()
  testExec()