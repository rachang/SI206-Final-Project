## SI 206 2017
## Final Project
import unittest
import itertools
import collections
import json
import sqlite3
import facebook
import api_access
import requests

fb_access_token = api_access.fb_access_token
graph = facebook.GraphAPI(fb_access_token, version="2.1")
# CACHE_FNAME = "finalproject.json"
# # Put the rest of your caching setup here:
# try:
#     cache_file = open(CACHE_FNAME,'r')# Try to read the data from the file
#     cache_contents = cache_file.read()# If it's there, get it into a string
#     cache_file.close()# Close the file, we're good, we got the data in a dictionary.
#     CACHE_DICTION = json.loads(cache_contents)# And then load it into a dictionary
# except:
#     CACHE_DICTION = {}
# def get_user_tweets(user):
# 	#caching data
# 	if user in CACHE_DICTION:
# 		results = CACHE_DICTION[user]
# 	#fetching data from twitter	
# 	else:
# 		#20 tweets from user timeline
# 		results = graph.get_connections(id=user, connection_name='friends')
# 		CACHE_DICTION[user] = results
# 		dumped_json_cache = json.dumps(CACHE_DICTION)
# 		fw = open(CACHE_FNAME,"w")
# 		fw.write(dumped_json_cache)
# 		fw.close() # Close the open file
# 	# return data that was retrieved from Twitter. 
# 	return results
# umich_tweets = get_user_tweets("10210997680568343")
# results = graph.get_connections(id="10210997680568343", connection_name='friends', limit=100)
# print(results)
graph = facebook.GraphAPI(fb_access_token)
profile = graph.get_object('me', fields = 'name,location') #fields is an optional key word argument
# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
print(json.dumps(profile, indent = 4))