"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from web import app
import json
import time
import lsnr
current_milli_time = lambda: int(round(time.time() * 1000))
# print (current_milli_time())


@app.route('/')
def root():
    return homes()
    
@app.route('/home')
def homes():
    """Renders the home page."""
    return render_template(
        'index.jade',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
    
@app.route('/test')
def testw():
    """print json"""
    start = current_milli_time()
    dbList = lsnr.appContext.db.queryAll("select * from test2")
    print("cost:" , (current_milli_time()-start))
    return json.dumps(dbList)
