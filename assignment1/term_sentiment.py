import sys
import json
import re
from operator import add

def main():
    #open the sentiment data and format it into a dictionary
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.


    #Create an empty dictionary to store our new sentiment terms and scores
    new_sentiment = {}
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
            if word in scores:
                sentiment += scores[word]
                    
        #Now we have the sentiment of the tweet, we work backwards to assign sentiment to words not in the original dictionary
        #We assume if it is regularly associated with negative sentiment tweets, it is a negative word
        
        #If sentiment is 0 we gain nothing useful from the tweet
        if sentiment == 0:
            continue
        #Define sentiment of new words as (count of times when words in a positive context  - count in a negative context) / # of occurences
        # sentiment > 0 => positive, < 0 => negative
        for word in text.split():
            #Boolean to test if word is in original dictionary
            contains = False
            if word in scores:
                contains = True
            #If it is in original dict, skip word
            if contains:
                continue
            if word in new_sentiment:
                new_sentiment[word] = map(add, new_sentiment[word], [sentiment, 1])
            else:
                new_sentiment[word] = [sentiment, 1]
                
    #Output new_sentiment dict
    for word, list in new_sentiment.iteritems():
        print "{} {}".format(word, list[0] / list[1])
                                         
if __name__ == '__main__':
    main()
