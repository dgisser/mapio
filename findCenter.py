
#dies on -180->180
def findCenterSimple(listOfLocs):
	centLat = 0
	centLong = 0
	
	#simple mean
	for loc in listOfLocs:
		centLat += loc[0]
		centLong += loc[1]

	centLat /= len(listOfLocs)
	centLong /= len(listOfLocs)

	return (centLat, centLong)

def calcCenterThreePoints(loc1, loc2, loc3):
	x1 = loc1[0];
	y1 = loc1[1];
	x2 = loc2[0];
	y2 = loc2[1];
	x3 = loc3[0];
	y3 = loc3[1];

	m1 = (y2-y1)*1.0/(x2-x1)
	m1p = 1.0/(-m1)
	c1p = (y2+y1)/2.0-m1p*(x2+x1)/2.0


	m2 = (y2-y3)*1.0/(x2-x3)
	m2p = 1.0/(-m2)
	c2p = (y2+y3)/2.0-m2p*(x2+x3)/2.0

	if ( m2p == m1p ):
		d1 = (x2-x1)**2 + (y2-y1)**2
		d2 = (x2-x3)**2 + (y2-y3)**2
		d3 = (x3-x1)**2 + (y3-y1)**2
		if ( d1 >= d2 ):
			if ( d1 >= d3):
				return [((x2+x1)/2., (y2+y1)/2.),d1**0.5]
			else:
				return [((x3+x1)/2., (y3+y1)/2.),d2**0.5]
		else:
			if ( d2 >= d3 ):
				return [((x2+x3)/2., (y2+y3)/2.),d2**0.5]
			else:
				return [((x1+x3)/2., (y1+y3)/2.),d2**0.5]


	yi = (m2p/m1p*c1p-c2p)*m1p/(m2p-m1p)
	xi = (yi-c2p)/m2p
	rad = pow((x1-xi)**2 + (y1-yi)**2, 0.5)/2.0

	return [(xi,yi),rad]

def distance(loc1, loc2):
	return pow((loc1[0]-loc2[0])**2.0 + (loc1[1]-loc2[1])**2.0, 0.5 )

def calcCenterTwoPoints(loc1, loc2):
	x1 = loc1[0];
	y1 = loc1[1];
	x2 = loc2[0];
	y2 = loc2[1];
	return [((x1+x2)/2., (y1+y2)/2.),pow((x2-x1)**2+(y2-y1)**2, 0.5)/2.]


def findCenterMinLargest(listOfLocs):
 	
	bestCirc = [(0,0),10000000000000000]

 	for c in range(0,len(listOfLocs)):
 		for d in range(0,len(listOfLocs)):
 			if ( c == d):
 				continue
 			#do the two case
 			currCirc = calcCenterTwoPoints(listOfLocs[c], listOfLocs[d])
 			works = True
 			for e in range(0,len(listOfLocs)):
 				if ( distance(currCirc[0], listOfLocs[e]) > currCirc[1] ):
 					works = False
 					break
 			if (works and (bestCirc[1] > currCirc[1]) ) :
 				bestCirc = currCirc

 			for f in range(0,len(listOfLocs)):
 				if ( f == d ):
 					continue
 				
 				currCirc = calcCenterThreePoints(listOfLocs[c], listOfLocs[d], listOfLocs[f])
 				for e in range(0,len(listOfLocs)):
 					if ( distance(currCirc[0], listOfLocs[e]) > currCirc[1] ):
 						works = False
 						break
 				if (works and (bestCirc[1] > currCirc[1])):
 					bestCirc = currCirc

 	return bestCirc






















