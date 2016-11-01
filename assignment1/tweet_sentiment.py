import sys
import json
import re

def main():
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
        #access the text of the tweet
        text = f[u'text']

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
                    
        print(sentiment)
                                     
if __name__ == '__main__':
    main()
