
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

def calcCenterThreePoints(x1,y1,x2,y2,x3,y3):

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
	rad = pow((x1-xi)**2 + (y1-yi)**2, 0.5)

	return [(xi,yi),rad]


def smallestCircle(listToProc, lenToProc, listProcced, currCenter, currRadius):
	if ( lenToProc == 0 ):
		return (currCenter,currRadius)
	
	newPoint = listToProc[lenToProc-1]

	if ( pow(pow( (newPoint[0]-currCenter[0]), 2) + pow( (newPoint[1]-currCenter[1]), 2),0.5) <= currRadius):
		return smallestCircle(listToProc, lenToProc-1, listProcced, currCenter, currRadius)

	res = []
	res.append( calcCenterThreePoints(newPoint[0], newPoint[1], listProcced[1][0], listProcced[1][1], listProcced[2][0], listProcced[2][1]) )
	res.append( calcCenterThreePoints(newPoint[0], newPoint[1], listProcced[0][0], listProcced[0][1], listProcced[2][0], listProcced[2][1]) )
	res.append( calcCenterThreePoints(newPoint[0], newPoint[1], listProcced[0][0], listProcced[0][1], listProcced[1][0], listProcced[1][1]) )

	idx = 0
	min = res[0][1]
	for x in range(0,2):
		if ( res[x][1] < min):
			min = res[x][1]
			idx = x

	listProcced[idx] = newPoint
	return smallestCircle(listToProc, lenToProc-1, listProcced, res[idx][0], res[idx][1])

	return res[idx]

def findCenterMinLargest(listOfLocs):
 	if ( len(listOfLocs) < 3 ):
 		retLat = 0.0
 		retLong = 0.0
 		for loc in listOfLocs:
 			retLat += loc[0]
 			retLong += loc[1]
 		retLat /= len(listOfLocs)
 		retLong /= len(listOfLocs)

 		return (retLat,retLong)

 	centerInfo = calcCenterThreePoints(listOfLocs[0][0],listOfLocs[0][1],listOfLocs[1][0],listOfLocs[1][1], listOfLocs[2][0],listOfLocs[2][1])
 	initCenter = centerInfo[0]
 	initRadius = centerInfo[1]

 	listProcced = listOfLocs[0:3]

 	return smallestCircle(listOfLocs, len(listOfLocs), listProcced, initCenter, initRadius)