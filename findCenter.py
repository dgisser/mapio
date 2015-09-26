
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


#def findCenterMinLargest(listOfLocs):
