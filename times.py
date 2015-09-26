import googlemaps
from restaurants import search

def getTimes(ll,peeps):
    key = 'AIzaSyDrXFWbkfQSZ9ayLS-XUWjOnKrs1x440eA'
    client = googlemaps.Client(key)
    if not ll:
        ll="40.4435480,-79.9446180"
    term=""
    rests=search(term, ll)

    businesses = rests.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, ll)
        quit()

    ndes=len(businesses)
    origins=peeps

    destinations=[]
    for x in range(ndes):
        destinations.append( {
            'lat' : businesses[x]['location']['coordinate']['latitude'],
            'lng' : businesses[x]['location']['coordinate']['longitude']
        } )

    matrix = client.distance_matrix(origins, destinations,
            mode="driving",
            units="imperial",
            departure_time="now")

    # times = [[1,2,3],[4,5,6]], where 1,2,3 are the amounts of time it takes for the first person to get to shop 1, shop 2, and shop 3 respectively, and 4,5,6 are the times it takes for person 2 to go to shop 1, shop 2, and shop 3.
    times=[]
    ind=0
    for pers in matrix['rows']:
        times.append([])
        for place in pers['elements']:
            times[ind].append(place['duration']['text'])
        ind+=1

    return times
