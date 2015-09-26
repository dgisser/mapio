import urllib, ast, json
def getLocation():
	url='http://freegeoip.net/json/'	
	response=urllib.urlopen(url).read()
	response=ast.literal_eval(response)
	lon=response['longitude']
	lat=response['latitude']
	d={'lon':lon,'lat':lat}
	return d