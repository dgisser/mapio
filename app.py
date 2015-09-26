import os
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import expanduser
from flask import Flask, url_for, redirect, render_template, request, abort
from flask.ext.stormpath import StormpathManager
from flask.ext.stormpath import login_required, user
from stormpath.cache.redis_store import RedisStore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'someprivatestringhere'
app.config['STORMPATH_API_KEY_FILE'] = expanduser('~/.stormpath/apiKey-2NUNTODZJKPTFOZ7PJADHYL01.properties')
app.config['STORMPATH_APPLICATION'] = 'mapio'
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True
app.config['STORMPATH_ENABLE_MIDDLE_NAME'] = False
app.config['STORMPATH_ENABLE_FACEBOOK'] = True
app.config['STORMPATH_REGISTRATION_REDIRECT_URL'] = '/registered'
app.config['STORMPATH_ENABLE_GOOGLE'] = True

stormpath_manager = StormpathManager(app)
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = "users"
  user_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.Text, unique=True)

  def __init__(self, email):
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.email

@app.route('/registered')
@login_required
def registered():
    userObj = User(user.email)
    db.session.add(userObj)
    db.session.commit()
    return "email added to db"

@app.route('/')
def home():
  if not user.is_authenticated():
    return 'home page!'
  else:
    return user.email

if __name__ == '__main__':
    app.run(host='0.0.0.0')
