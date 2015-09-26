import re,requests
def getLocation():
	raw = requests.get('http://www.geoiptool.com/').text
	latlon = re.search("GPoint\(([^)]+)\)",raw).groups(0)
	lat,lon = map(float,latlon[0].split(","))
	map={}
	map['lat']=lat
	map['lon']=lon
	return map