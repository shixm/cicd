# coding=utf-8
'''
@author: shixi
'''

import Conf  
import subprocess
import sys
from  LLog import Logger
log = Logger("itexec").getLogger()


class itexec(object):

    def __init__(self):
        print (sys.path)
        pass

    def _getSubP(self,):
        return subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def dox(self, cmd):
        subp = subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        cmd_out = ""
        try:
            subp.stdin.write(cmd)
        finally:
            subp.stdin.close()
        try:   
            for line in subp.stdout:
                cmd_out += line
        finally:
            subp.stdout.close()
        try:   
            cmd_error = subp.stderr.readlines()
        finally:
            subp.stderr.close()
            
        log.debug("subp|%s|%s|%s|", cmd, cmd_out, cmd_error)
    
    def do1(self, cmd):
        kk = subprocess.getstatusoutput(cmd)
#       kk =subprocess.Popen(cmd)
        log.debug("do1|%s|%s|%s|", cmd, kk[0], kk[1])

    def do(self):
        pass
    
    
if __name__ == '__main__':
    print(Conf)
    log.debug("----------------------")
    it = itexec()
    it.do1("c: & cd  c:/users/shixi & dir")
    it.do1("dir")
    it.dox("dir")
    it.dox("dir&C:&dir")
    log.debug("----------------------")
    it.do1("dir")
    
    pass
