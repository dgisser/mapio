from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template
import os, json
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import expanduser
from flask import Flask, url_for, redirect, render_template, request, abort,Response
from flask.ext.stormpath import StormpathManager
from flask.ext.stormpath import login_required, user
from stormpath.cache.redis_store import RedisStore
from restaurants import search,get_business
from findCenter import findCenterMinLargest
from times import getTimes
import urllib2
from sqlalchemy import create_engine
from geoalchemy2 import Geography

app = Flask(__name__)

engine = create_engine('postgresql://gis:gis@localhost/gis', echo=True)
app.config['STORMPATH_SOCIAL'] = {'FACEBOOK': {'app_id': "169054186767605",'app_secret': "023a3dd0cf832d80249d863baec5fef8",},'GOOGLE': {'client_id': "421392893604-t796vp3jjggvc2t296i80v5dhfvch03j.apps.googleusercontent.com",'client_secret': "5EufqXkFoR-fyJI_7Ok1oWdC",}}
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
  location = db.Column(Geography('Point,4326'))

  def __init__(self, email):
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.email

class Group(db.Model):
  __tablename__ = "groups"
  group_id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String(10), UNIQUE(key));

  def __init__(self, key):
    self.key = key

  def __repr__(self):
    return '<Group %r>' % self.key


@app.route('/registered')
@login_required
def registered():
    userObj = User(user.email)
    db.session.add(userObj)
   # db.session.commit()
    return render_template("home.html")

dest =  [-33.8, 150.5];

listOfOrigin = [[40.890542, -81.274856, 4],[39.923036, -80.259052, 5],[40.028249, -81.157507, 3],[39.80010128657071, -81.28747820854187, 2], [40.950198, -81.259302, 1]]


@app.route("/", methods=['post','get'])
def hello():
	if request.method=='POST':
		cLat=float(request.form['lat'])
		cLon=float(request.form['lon'])
		newl=[]
		newl.append(cLat)
		newl.append(cLon)
		boo=True
		for i in listOfOrigin:
			if(i[0]==cLat and i[1]==cLon):
				boo=False
		if(boo):
			listOfOrigin.append(newl)

	ll=findCenterMinLargest(listOfOrigin)[0]
	term=""
	businessJson=yelpSearch(ll,term)
	teles=timeSearch(ll)
        print(ll[0])

	return render_template('home.html',dest=businessJson,teles3=teles,listOfOrigin=listOfOrigin,latC=ll[0],lngC=ll[1])

@app.route("/search",methods=['post'])
def returnSearch():
	assert request.method=='POST'
	searchTerm=request.form['searchTerm']
	ll=findCenterMinLargest(listOfOrigin)[0]
	businessJson=yelpSearch(ll,searchTerm)
        teles=timeSearch(ll)
	return render_template('home.html',dest=businessJson,teles3=teles,listOfOrigin=listOfOrigin,latC=ll[0],lngC=ll[1])

def yelpSearch(ll, term):
	try:
		busDict=search(term, str(ll[0])+","+str(ll[1]))
	except urllib2.HTTPError as error:
		sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

	businesses=busDict.get('businesses')
	businessList=[]
	print(businesses)
	for i in businesses:
		url=i['url']
		name=i['name']
		loc=i['location']
		rating=i['rating']
		cBus={}
		if 'image_url' in i.keys():
			image=i['image_url']
			cBus["image_url"]=image
		else:
			cBus["image_url"]=None
                if 'rating_img_url' in i.keys():
                        rating_url=i['rating_img_url']
                        cBus['rating_images_url']=rating_url
                else:
                        cBus['irating_images_url']=None
                lat=loc['coordinate']['latitude']
		lng=loc['coordinate']['longitude']
		address=loc['display_address']
		cBus["rating"]=rating
		cBus["url"]=url
		cBus["name"]=name
		cBus["lat"]=lat
		cBus["lng"	]=lng
		cBus["rer"]=i['review_count']
                cBus["add"]=address
		businessList.append(cBus)

	businessJson={}
	businessJson["businesses"]=businessList
	return json.dumps(businessJson)

def timeSearch(ll):
        ele=getTimes(str(ll[0])+","+str(ll[1]),listOfOrigin)
        eleJson={}
        eleJson['rows']=ele
        return json.dumps(eleJson)

if __name__ == '__main__':
    app.run(debug=True)
