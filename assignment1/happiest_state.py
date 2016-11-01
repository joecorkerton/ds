import sys
import json
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, (lat2, lon2, _)):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def main():
    #Define dict with states and their average lat,long
    states = {
        'AK': [61.3850,-152.2683, 0],
        'AL': [32.7990,-86.8073, 0],
        'AR': [34.9513,-92.3809, 0],
        'AS': [14.2417,-170.7197, 0],
        'AZ': [33.7712,-111.3877,0 ],
        'CA': [36.1700,-119.7462, 0],
        'CO': [39.0646,-105.3272, 0],
        'CT': [41.5834,-72.7622, 0],
        'DC': [38.8964,-77.0262, 0],
        'DE': [39.3498,-75.5148, 0],
        'FL': [27.8333,-81.7170, 0],
        'GA': [32.9866,-83.6487, 0],
        'HI': [21.1098,-157.5311, 0],
        'IA': [42.0046,-93.2140, 0],
        'ID': [44.2394,-114.5103, 0],
        'IL': [40.3363,-89.0022, 0],
        'IN': [39.8647,-86.2604, 0],
        'KS': [38.5111,-96.8005, 0],
        'KY': [37.6690,-84.6514, 0],
        'LA': [31.1801,-91.8749, 0],
        'MA': [42.2373,-71.5314, 0],
        'MD': [39.0724,-76.7902, 0],
        'ME': [44.6074,-69.3977, 0],
        'MI': [43.3504,-84.5603, 0],
        'MN': [45.7326,-93.9196, 0],
        'MO': [38.4623,-92.3020, 0],
        'MP': [14.8058,145.5505, 0],
        'MS': [32.7673,-89.6812, 0],
        'MT': [46.9048,-110.3261, 0],
        'NC': [35.6411,-79.8431, 0],
        'ND': [47.5362,-99.7930, 0],
        'NE': [41.1289,-98.2883, 0],
        'NH': [43.4108,-71.5653, 0],
        'NJ': [40.3140,-74.5089, 0],
        'NM': [34.8375,-106.2371, 0],
        'NV': [38.4199,-117.1219, 0],
        'NY': [42.1497,-74.9384, 0],
        'OH': [40.3736,-82.77550, 0],
        'OK': [35.5376,-96.9247, 0],
        'OR': [44.5672,-122.1269, 0],
        'PA': [40.5773,-77.2640, 0],
        'PR': [18.2766,-66.3350, 0],
        'RI': [41.6772,-71.5101, 0],
        'SC': [33.8191,-80.9066, 0],
        'SD': [44.2853,-99.4632, 0],
        'TN': [35.7449,-86.7489, 0],
        'TX': [31.1060,-97.6475, 0],
        'UT': [40.1135,-111.8535, 0],
        'VA': [37.7680,-78.2057, 0],
        'VI': [18.0001,-64.8199, 0],
        'VT': [44.0407,-72.7093, 0],
        'WA': [47.3917,-121.5708, 0],
        'WI': [44.2563,-89.6385, 0],
        'WV': [38.4680,-80.9696, 0],
        'WY': [42.7475,-107.2085, 0]
}
    
    #open the sentiment data and format it into a dictionary
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    #load twitter data into a dictionary with json. Each line is a new tweet
    
    for line in tweet_file:
        f = json.loads(line)
        
        #If data doesn't have text for a tweet, skip it
        if u'text' not in f:
            continue
        #If tweet isn't english, skip it
        if u'lang' not in f:
            continue
        if f[u'lang'] != u'en':
            continue
        #access the text of the tweet
        text = f[u'text']
        
        if f[u'coordinates']:
            #Check if this is in the US
            coords = f[u'coordinates'][u'coordinates']
            
            if coords[1] > 49 or coords[1] < 25:
                continue
            elif coords[0] > -68 or coords[0] < -124:
                continue
            else:
                closest = 1E8
                #Data in form [longitude, latitude]
                #Loop through states, finding which is closest
                for code, longlat in states.iteritems():
                    distance = haversine(coords[1], coords[0], states[code]) 
                    if  distance < closest:
                        closest = distance
                        state = code
        else:
            continue

        #Discard any non ASCII characters
        text = text.encode('ascii','ignore')
        #Sentiment score of the tweet
        sentiment = 0
        
        #Loop through words in text, seeing if each is in the sentiment dictionary
        for word in text.split():
            for term, score in scores.iteritems():
                if word == term:
                    sentiment += score
                    break
                    
        states[state][2] += sentiment
        
    #Find the state with the highest sentiment and output
    max = -1E6
    for state, count in states.iteritems():
        current = states[state][2]
        if current > max:
            max = current
            top = state
    
    print top 
                                     
if __name__ == '__main__':
    main()
