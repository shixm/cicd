# coding=utf-8

# import MySQLdb
import Conf
import pymysql
from  LLog import Logger

  
log = Logger("db").getLogger()

class dbUtil:  
    def __init__(self, host, user, password, charset="utf8"):  
        self.host = host  
        self.user = user  
        self.password = password  
        self.charset = charset  
        try:  
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.password)  
            self.conn.set_charset(self.charset)  
            self.cur = self.conn.cursor()  
        except pymysql.Error as e:  
            log.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            raise  e  
  
  
    def selectDb(self, db):  
        try:  
            self.conn.select_db(db)  
        except pymysql.Error as e:  
            log.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))  
  
    def query(self, sql):  
        try:  
            n = self.cur.execute(sql)  
            return n  
        except pymysql.Error as e:  
            log.error("Mysql Error:%s\nSQL:%s" % (e, sql))  
  
    def execs(self, sql):  
        try:  
            n = self.cur.execute(sql)  
            return n  
        except pymysql.Error as e:  
            log.error("Mysql Error:%s\nSQL:%s" % (e, sql)) 
            raise e 
    def execsNraise(self, sql):  
        try:  
            n = self.cur.execute(sql)  
            return n  
        except pymysql.Error as e:  
            log.error("Mysql Error:%s\nSQL:%s" % (e, sql)) 
  
  
    def queryRow(self, sql):  
        self.query(sql)  
        result = self.cur.fetchone()  
        return result  
  
    def queryAll(self, sql):  
        self.query(sql)  
        result = self.cur.fetchall()  
        desc = self.cur.description  
        d = []  
        for inv in result:  
            _d = {}  
            for i in range(0, len(inv)):  
                _d[desc[i][0]] = str(inv[i])  
            d.append(_d)  
        return d  
  
    def insert(self, p_table_name, p_data):  
        for key in p_data:  
            p_data[key] = "'" + str(p_data[key]) + "'"  
        key = ','.join(p_data.keys())  
        value = ','.join(p_data.values())  
        real_sql = "INSERT INTO " + p_table_name + " (" + key + ") VALUES (" + value + ")"  
#         self.query("set names 'utf8'")  
        return self.query(real_sql)  
  
  
    def getLastInsertId(self):  
        return self.cur.lastrowid  
  
    def rowcount(self):  
        return self.cur.rowcount  
  
    def commit(self):  
        self.conn.commit()  
  
    def close(self):  
        self.cur.close()  
        self.conn.close()
if __name__ == "__main__":
    print("main")
    db = dbUtil(Conf.dbHost, Conf.dbUser, Conf.dbPass)
    db.selectDb("test")
    db.execs("delete from test2")
    db.insert("test2", {"ids":'2',"names":"workd"})
    dbList = db.queryAll("select * from test2")
    db.commit()
    print(dbList)
