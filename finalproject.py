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
from datetime import datetime
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
fbposts = get_Facebook(fb_user)

conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Facebook_Posts")

cur.execute('''CREATE TABLE Facebook_Posts (user_id TEXT, created_time DATETIME, weekday TEXT, message TEXT, story TEXT)''')
for posts in fbposts["data"]:
	user_id = posts["id"]
	created_time = posts["created_time"]
	created_time = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S%z")
	weekday = datetime.strftime(created_time,"%A")
	if "story" in posts:
		story = posts["story"]
	else:
		story = ""
	if "message" in posts:
		message = posts["message"]
	else:
		message = ""
	print(created_time, weekday)


	cur.execute('''INSERT or IGNORE INTO Facebook_Posts (user_id, created_time, weekday, message, story) VALUES (?,?,?,?,?)'''
		, (user_id, created_time, weekday, message, story))
conn.commit()
cur.close()