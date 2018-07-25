#coding=utf-8

import os
import sys
import logging
from logging.handlers import MemoryHandler, RotatingFileHandler

import fileutil
# from cleanmaster_sync.config import Path

class Logger:

    def __init__(self, name, size = 10, backupCount = 50, cacheRecords = 1, print_to_console=True): 
        '''  size : 单个日志文件的大小，单位是M。
             backupCount :备份的最大日志文件数'
             cacheRecords :日志缓存数。达到该数字才会写硬盘。flushLevel以上级别的除外'''
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        logdir = os.path.join(os.path.dirname(__name__), "logs")
#         logdir = os.path.join(Path.LOG, name)
        fileutil.ensure_dir_exists(logdir)
        logfile = os.path.join(logdir, '%s.log' % name)
        hdlr = RotatingFileHandler(logfile, 'a', maxBytes=1024 * 1024 *size, backupCount=backupCount)
        hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        mh = MemoryHandler(cacheRecords,flushLevel=logging.INFO, target=hdlr) #flushLevel（包含）以上级别的立刻写硬盘
        self.logger.addHandler(mh)
        if print_to_console:
            #将大于或等于DEBUG级别的信息输出到控件台
            hdlr = logging.StreamHandler(sys.stdout)
            hdlr.setFormatter(logging.Formatter("%(message)s", ""))
            hdlr.setLevel(logging.DEBUG)
            self.logger.addHandler(hdlr)
        self.logger.print=self.logger.debug

    def getLogger(self):
        return self.logger
    
if  __name__ == "__main__":
    log = Logger("logs").getLogger()
    log.debug("test")
    
        
