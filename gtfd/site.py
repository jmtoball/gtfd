from flask import Flask
from flaskext.mail import Mail
from gtfd.db import db_session, init_db
from datetime import datetime, timedelta
from gtfd import conf

app = Flask(__name__)
app.config.from_object(conf)
mail = Mail(app)
init_db()

import gtfd.views.main
import gtfd.views.login

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response
