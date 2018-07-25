'''
Created on 2018年7月16日

@author: shixi
'''
import lsnr
plus=lambda a,b: a+b

if __name__ == '__main__':
    print(plus(1,2))
    app = lsnr.appContext
    print(app)
    app = lsnr.appContext
    print(app)
    app = lsnr.fa.Lsnrctl()
    app.start()
    print(app)
