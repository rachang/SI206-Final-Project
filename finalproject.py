## SI 206 2017
## Final Project
import unittest
import itertools
from collections import Counter
import json
import sqlite3
import facebook
import api_access
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
CACHE_FNAME = "fbfinalproject.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')# Try to read the data from the file
    cache_contents = cache_file.read()# If it's there, get it into a string
    cache_file.close()# Close the file, we're good, we got the data in a dictionary.
    CACHE_DICTION = json.loads(cache_contents)# And then load it into a dictionary
except:
    CACHE_DICTION = {}

#facebook access token and user id linked from access_token.py
fb_access_token = api_access.fb_access_token
fb_user = api_access.fb_user

#requests setup for the last 100 posts on my user feed 
fb_url = "https://graph.facebook.com/v2.11/" + fb_user + "/feed"
url_params = {}
url_params["access_token"]= fb_access_token
url_params["limit"]= 100 

def get_Facebook(user):
	#data already in cache
	if user in CACHE_DICTION:
		print("retrieving from cache")
		results = CACHE_DICTION[user]
	#data not already in cache, fetching results as json from Facebook
	else:
		print("fetching from facebook")
		results = requests.get(fb_url, params=url_params)
		CACHE_DICTION[user] = json.loads(results.text)
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
	# return data that was retrieved from Facebook. 
	return results
fbposts = get_Facebook(fb_user)
#create Database for project
conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()
#create table within database for Facebook API
cur.execute("DROP TABLE IF EXISTS Facebook_Posts")
cur.execute('''CREATE TABLE Facebook_Posts (post_id TEXT, created_time DATETIME, weekday TEXT, timeperiod TEXT, message TEXT, story TEXT)''')
#looping through every post and retrieving the post id, created time, message, story
#from created time, finding the weekday and time period
for posts in fbposts["data"]:
	post_id = posts["id"]
	created_time = posts["created_time"]
	#converting created_time to datetime syntax
	created_time = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S%z")
	#finding weekday from created_time
	weekday = datetime.strftime(created_time,"%A")
	#finding time of day from created_time and categorizing time of day into 4 time periods
	timeofday = int(datetime.strftime(created_time, "%H%M"))
	timeperiod = ""
	if timeofday >= 0 and timeofday <= 559:
		timeperiod = "Early Morning"
	elif timeofday >= 600 and timeofday <= 1159:
		timeperiod = "Morning"
	elif timeofday >= 1200 and timeofday <= 1759:
		timeperiod = "Afternoon"
	else:
		timeperiod = "Night" 
	#some posts only have stories, some only have messages, some have both
	if "story" in posts:
		story = posts["story"]
	else:
		story = ""
	if "message" in posts:
		message = posts["message"]
	else:
		message = ""
	#writing in all 6 columns into table
	cur.execute('''INSERT or IGNORE INTO Facebook_Posts (post_id, created_time, weekday, timeperiod, message, story) VALUES (?,?,?,?,?,?)'''
		, (post_id, created_time, weekday, timeperiod, message, story))
conn.commit()
#datetime report of days most active on Facebook
activity_by_day = []
activity_by_time_period = []
total_activity =[]
weekday = cur.execute("SELECT weekday, timeperiod FROM Facebook_Posts")
for row in weekday:
	activity_by_day.append(row[0])
	activity_by_time_period.append(row[1])
	total_activity.append(row)

print("Activity tracked by day: \n", Counter(activity_by_day))
print("Activity tracked by time period: \n", Counter(activity_by_time_period))
print("Activity tracked by day and time period combined: \n", Counter(total_activity))
cur.close()