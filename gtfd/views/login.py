from flaskext.openid import OpenID
from gtfd.site import app
from flask import request, redirect, flash, url_for, g, session
from gtfd.db import User, Auth, db_session
from gtfd.conf import VELRUSE_URL
from gtfd.views.common import render
import simplejson

import urllib2

def populate_user():
    if session and 'uid' in session:
        g.user = User.query.filter(User.id==session['uid']).first()
    else:
        g.user = None

app.before_request(populate_user)

def loginExistingUser(user):
    flash('Signed in - let\'s kick some ass!')
    session['uid'] = user.id

def createUser(prf):
    email = ""
    if "verifiedEmail" in prf:
        email = prf['verifiedEmail']
    elif "emails" in prf and len(prf['emails']):
        email = prf['emails'][0]
    name=prf['displayName']
    if type(name).__name__ == 'list':
        name = name[0]
    user = User(name, email=email)
    db_session.add(user)
    db_session.commit()
    return user

def addConnection(prf, user):
    auth = Auth(auth=prf['identifier'], uid=user.id)
    db_session.add(auth)
    db_session.commit()

def connectNewUser(prf):
    print "User: "+str(g.user)
    if g.user == None:
        user = createUser(prf)
    else:
        user = g.user
    addConnection(prf, user)
    session['uid'] = user.id
    flash('Welcome to GTFD - Add some tasks!')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if "token" in request.form:
            token = request.form["token"]
            resp = urllib2.urlopen(VELRUSE_URL+"auth_info/?token="+token).read()
            if resp:
                data = simplejson.loads(resp)
                if data['status'] == "fail":
                    flash('Login failed: '+data['reason']['description'], 'error')
                    return redirect(url_for("home"))
                prf = data['profile']

                auth = Auth.query.filter_by(auth=prf['identifier']).first()
                if auth is not None:
                    loginExistingUser(auth.user)
                    return redirect(url_for("home"))
                else:
                    connectNewUser(prf)                
                    return redirect(url_for('home'))
    return render('login.html')

@app.route('/logout/')
def logout():
    session.pop('uid', None)
    flash('Signed out - you can run, but you cannot hide!')
    return redirect(url_for('home'))

