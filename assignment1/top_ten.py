import json
import sys
import operator

def main():
    #Get the input twitter data
    tweet_file = open(sys.argv[1])
    
    #Initialize hashtag frequency dictionary
    hash_freq = {}
    
    #For each tweet 
    for line in tweet_file:
        f = json.loads(line)
        
        #If tweet doesn't contain any hashtags, skip it
        if u'entities' not in f:
            continue
        if not f[u'entities'][u'hashtags']:
            continue
        
        #Get the hashtags, add them to the frequency dict
        for hashtag in f[u'entities'][u'hashtags']:
            #Hashtags in form indices, text
            hashtag = hashtag[u'text']#.encode('ascii','ignore')
            if hashtag in hash_freq:
                hash_freq[hashtag] += 1
            else: 
                hash_freq[hashtag] = 1
                
    #Sort the dictionary by the frequency in descending order, and output the top ten    
    sorted_freq = sorted(hash_freq.items(), key=operator.itemgetter(1), reverse = True)[:10]
    
    for x in range(len(sorted_freq)):
        print u"{} {}".format(sorted_freq[x][0], sorted_freq[x][1])    
        
        
if __name__ == '__main__':
    main()
