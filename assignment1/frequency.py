from __future__ import division #Need floating point divison
import sys
import json



def main():
    #Get the input twitter data
    tweet_file = open(sys.argv[1])
    
    #Initialize dict to count word frequency
    word_freq = {}
    
    #Variable to count total number of words
    total = 0
    
    #For each tweet, get the text
    for line in tweet_file:
        f = json.loads(line)
        
        #If data doesn't have text for a tweet, skip it
        if u'text' not in f:
            continue
        #access the text of the tweet
        text = f[u'text']

        #Discard any non ASCII characters
        text = text.encode('ascii','ignore')
        
        #For each word, add one to count or add it to dictionary
        for word in text.split():
            total += 1
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        
        #Now output the results     
        for word, count in word_freq.iteritems():
            print "{} {}".format(word, count / total)
        
        
if __name__ == '__main__':
    main()
    
