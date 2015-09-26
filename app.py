from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
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
app.config['STORMPATH_ENABLE_FACEBOOK'] = False
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

listOfOrigin = [['Mark', -33.890542, 151.274856, 4], \
  ['Tom', -33.923036, 151.259052, 5], \
  ['Bob', -34.028249, 151.157507, 3], \
  ['Susan', -33.80010128657071, 151.28747820854187, 2], \
  ['Julie', -33.950198, 151.259302, 1] \
]

@app.route("/", methods=['post','get'])
def hello():
	if request.method=='POST':
		cLat=request.form['lat']
		cLon=request.form['lon']
		user.lat=cLat
		user.lon=cLon
		newl=[]
		newl.append("Ben")
		newl.append(cLat)
		newl.append(cLon)
		listOfOrigin.append(newl)
		for i in range(len(listOfOrigin)):
			print(listOfOrigin[i])

	return render_template('home.html',originList=listOfOrigin)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
