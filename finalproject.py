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
CACHE_FNAME = "finalproject.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')# Try to read the data from the file
    cache_contents = cache_file.read()# If it's there, get it into a string
    cache_file.close()# Close the file, we're good, we got the data in a dictionary.
    CACHE_DICTION = json.loads(cache_contents)# And then load it into a dictionary
except:
    CACHE_DICTION = {}
fb_access_token = api_access.fb_access_token
fb_user = api_access.fb_user
def get_Facebook(user):
	fb_url = "https://graph.facebook.com/v2.11/" + fb_user + "/feed"
	url_params = {}
	url_params["access_token"]= fb_access_token
	url_params["limit"]= 100 
	if user in CACHE_DICTION:
		print("fetching")
		results = CACHE_DICTION[user]
	else:
		print("caching")
		results = requests.get(fb_url, params=url_params)
		CACHE_DICTION[user] = json.loads(results.text)
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	# return data that was retrieved from Twitter. 
	return results
hello = get_Facebook(fb_user)

