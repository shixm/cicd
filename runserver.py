"""
This script runs the FlaskWebProject2 application using a development server.
"""
import  sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname(__file__)), 'comm'))
sys.path.insert(0, join(abspath(dirname(__file__)), 'lsnr'))
sys.path.insert(0, join(abspath(dirname(__file__)), 'web'))
for path in sys.path:
    print(path)

from os import environ
import logging
from web import app



if __name__ == '__main__':
    #init 2 
    app.debug = True
    
    handler = logging.FileHandler('./logs/flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
