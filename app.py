from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
import os, json
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import expanduser
from flask import Flask, url_for, redirect, render_template, request, abort
from flask.ext.stormpath import StormpathManager
from flask.ext.stormpath import login_required, user
from stormpath.cache.redis_store import RedisStore
from restaurants import search,get_business



app = Flask(__name__)

app.config['STORMPATH_SOCIAL'] = {'FACEBOOK': {'app_id': "169054186767605",'app_secret': "023a3dd0cf832d80249d863baec5fef8",},'GOOGLE': {'client_id': "421392893604-t796vp3jjggvc2t296i80v5dhfvch03j.apps.googleusercontent.com",'client_secret': "5EufqXkFoR-fyJI_7Ok1oWdC",}}
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
   # db.session.commit()
    return "email added to db"

dest =  [-33.8, 150.5];

listOfOrigin = [[-33.890542, 151.274856, 4],[-33.923036, 151.259052, 5],[-34.028249, 151.157507, 3],[-33.80010128657071, 151.28747820854187, 2], [-33.950198, 151.259302, 1]]


@app.route("/", methods=['post','get'])
def hello():
	if request.method=='POST':
		cLat=float(request.form['lat'])
		cLon=float(request.form['lon'])
		user.lat=cLat
		user.lon=cLon
		newl=[]
		newl.append(cLat)
		newl.append(cLon)
		newl.append(1)
		listOfOrigin.append(newl)
	ll={'lat':40.4435480,'lng':-79.9446180}
	term=""
	businessJson=yelpSearch(ll,term)

	return render_template('home.html',dest=businessJson,listOfOrigin=listOfOrigin)

def yelpSearch(ll, term):
	try:
		busDict=search(term, str(ll['lat'])+","+str(ll['lng']))
	except urllib2.HTTPError as error:
		sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

	businesses=busDict.get('businesses')
	businessList=[]
	for i in businesses:
		url=i['url']
		name=i['name']
		loc=i['location']
		lat=loc['coordinate']['latitude']
		lng=loc['coordinate']['longitude']
		address=loc['display_address']
		cBus={}
		cBus["url"]=url
		cBus["name"]=name
		cBus["lat"]=lat
		cBus["lng"	]=lng
		cBus["add"]=address
		businessList.append(cBus)

	businessJson={}
	businessJson["businesses"]=businessList
	return json.dumps(businessJson)

if __name__ == '__main__':
    app.run(debug=True)
