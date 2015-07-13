import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from sys import argv
import signal
import json
from sklearn.cluster import DBSCAN
import scipy.spatial
import numpy as np
from numpy import array
from shapely.geometry import MultiPoint
from simplekml import Kml, Style
import simplekml
from polycircles import polycircles
import pprint
import csv
import unicodedata

script, outfile = argv

product = open(outfile, 'a')

pp = pprint.PrettyPrinter(indent=4)

#Variables that contains the user credentials to access Twitter API 
access_token = "322768123-J4TtrQAdDiK2VkDXzKtcwunwGVyjfbiFLdLZK9oZ"
access_token_secret = "W7XNMbUwNl8YiwbowgEL5UQwRufVYHbEvCD8otaXq8isv"
consumer_key = "usRQFnlX4QkEpGPGV2jeOutOm"
consumer_secret = "z5NRrNKIwraVLYc2JB6kK8hdavq7u4zWk7KgXydDU4LJNODT4c"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweets = []

# Streamer
class MySteamListener(tweepy.StreamListener):

    def on_data(self, data):
        tweets.append(data)

myStream = Stream(auth, MySteamListener())

# TIMER
def handler(signum, frame):
    myStream.disconnect()


# Bounding Box Tester
def Bounding_Box_Test (lat, lon, north, south, east, west):
    if west <= lon <= east and south <= lat <= north:
        return "Yes"

    else:
        return "No"


# San Francisco Bounding Box
north = 37.835541
south = 37.707694
east = -122.349688
west = -122.518898

time = 120



# # Testing Stream Output 
# print "Starting Timer for %d seconds" % time
# signal.signal(signal.SIGALRM, handler)
# signal.alarm(time)

# myStream.filter(locations=[-122.550900,37.663574,-122.355846,37.843635])

# for item in tweets:

#     tweet = json.loads(item)

#     if tweet['coordinates'] != None:

#         print tweet['entities']['hashtags']



#Choosing Hashtags to Cluster

hashtags_to_cluster = []

hashtags_wanted = raw_input("Which hashtag are you looking for? ")

hashtags_to_cluster.append(hashtags_wanted)

more_hashtags = ""

while more_hashtags != "n":
    
    more_hashtags = raw_input("Want to add another hashtag? y or n ")

    if more_hashtags == "y":

        hashtags_wanted = raw_input("Which hashtag are you looking for? ")

        hashtags_to_cluster.append(hashtags_wanted)

print "Hashtags acquired, beginning search for %s" % [item for item in hashtags_to_cluster]



#By Desired Hashtag, with a set time.

tweets_with_desired_hash = []

print "Opening Stream for %d seconds" % time
signal.signal(signal.SIGALRM, handler)
signal.alarm(time)

myStream.filter(locations=[-122.550900,37.663574,-122.355846,37.843635])

for item in tweets:

    tweet = json.loads(item)
    # pp.pprint(tweet)

    if tweet['coordinates'] != None:

        if len(tweet['entities']['hashtags']) > 0:

            longitude = tweet['coordinates']['coordinates'][0]
            latitude = tweet['coordinates']['coordinates'][1]

            if Bounding_Box_Test(latitude, longitude, north, south, east, west) == "Yes":

                print [hashtag['text'].lower() for hashtag in tweet['entities']['hashtags']]

    #             if any(hashes in [hashtag['text'].lower() for hashtag in tweet['entities']['hashtags']] for hashes in hashtags_to_cluster):

    #                 tweets_with_desired_hash.append(tweet)

    #             else:
    #                 pass

    #         else:
    #             pass

    #     else:
    #         pass

    # else:
    #     pass


# print len(tweets_with_desired_hash)

# if len(tweets_with_desired_hash) > 0:
#     print tweets_with_desired_hash










# #By Minimum Number of Geocoded/Hashed Tweets 

# tweet_data_coords = []

# num_geo_hashed_tweets_wanted = int(raw_input("What's the minimum amount of tweets that are geocoded, from San Francisco and with hashtags, that you want? "))

# while len(tweet_data_coords) < num_geo_hashed_tweets_wanted:

#     print "Starting Timer for %d seconds" % time
#     signal.signal(signal.SIGALRM, handler)
#     signal.alarm(time)

#     myStream.filter(locations=[-122.550900,37.663574,-122.355846,37.843635])

#     for item in tweets:

#         tweet = json.loads(item)
#         # pp.pprint(tweet)

#         if tweet['coordinates'] != None:

#             if len(tweet['entities']['hashtags']) > 0:

#                 longitude = tweet['coordinates']['coordinates'][0]
#                 latitude = tweet['coordinates']['coordinates'][1]

#                 if Bounding_Box_Test(latitude, longitude, north, south, east, west) == "Yes":

#                     if latitude != 37.77493 and longitude != -122.419416:
                        
#                         tweet_data_coords.append(tweet)

#                     else:
#                         pass

#                 else:
#                     pass

#             else:
#                 pass

#         else:
#             pass




# # Simply by time
# print "Starting Timer for %d seconds" % time
# signal.signal(signal.SIGALRM, handler)
# signal.alarm(time)

# myStream.filter(locations=[-122.550900,37.663574,-122.355846,37.843635])

# for item in tweets:

#     tweet = json.loads(item)
#     # pp.pprint(tweet)

#     if tweet['coordinates'] != None:

#         if len(tweet['entities']['hashtags']) > 0:
#             tweet_data_coords.append(tweet)

#         else:
#             pass

#     else:
#         pass





# # PRINTING THE RESULTS OF THE STREAM
# print "Number of Tweets:", len (tweets)
# print "Number of Geo-located, Hash-Tagged Tweets in San Francisco:", len(tweet_data_coords)









# Reviewing Tweet Content/Keys
# pp.pprint(tweet_data_coords[0].keys())
# pp.pprint(tweet_data_coords[0]['user'])


# # Entering Filtered Data into Array of Dictionaries
# outputdata = []
# filtered_data = dict();

# for twit in tweet_data_coords:
#     filtered_data = {}

#     filtered_data['tweet_id'] = twit['id_str']

#     filtered_data['tweet_text'] = twit['text'].encode('"utf-8"', 'ignore')

#     filtered_data['date_created'] = twit['created_at']
 
#     tweet_hashes = []
#     tweet_hashes.append([hashtag['text'].lower().encode('"utf-8"', 'ignore') for hashtag in twit['entities']['hashtags']])
#     filtered_data['hashtags'] = tweet_hashes[0]

#     filtered_data['user_name'] = twit['user']['name'].encode('"utf-8"', 'ignore')

#     filtered_data['latitude'] = twit['coordinates']['coordinates'][1]

#     filtered_data['longitude'] = twit['coordinates']['coordinates'][0]

#     # # Hashtags as one string
#     # filtered_data['hashtags'] = ', '.join([hashtag['text'].lower() for hashtag in twit['entities']['hashtags']])

#     outputdata.append(filtered_data)



# # New Duplicate Cleaner using just the ID column
# unique_rows = {row['tweet_id']:row for row in outputdata}.values()



# print "Number of Unique, Geo-located, Hash-Tagged Tweets in San Francisco:", len(unique_rows)
# print "Percent of Total Tweets Getting Used: %d%%" % int(100 * (float(len(unique_rows))/float(len(tweets))))

# print unique_rows


# # Writing Everything Down
# fieldnames = (['tweet_id', 'user_name', 'date_created', 'tweet_text', 'hashtags',
#     'latitude', 'longitude'])

# writer = csv.DictWriter(product, dialect='excel', fieldnames=fieldnames, 
#     extrasaction='ignore', quoting=csv.QUOTE_NONNUMERIC)

# headers = dict( (n,n) for n in fieldnames )

# writer.writerow(headers)

# for row in unique_rows:
#     writer.writerow(row)

# product.close()









