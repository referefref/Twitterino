

# Prints out most recent Tweets posted by the user to the serail port 

import httplib
import json
import requests
from requests_oauthlib import OAuth1
import time
import serial 

s = serial.Serial(port='/dev/ttyUSB1', baudrate=9600)

# Get the following values from the OAuth tool in your Twitter app dashboard.
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
r = requests.get('https://userstream.twitter.com/1.1/user.json',
    params={'replies': 'all', 'delimited': 'length'}, stream=True, auth=auth)

last_request = time.time()
for line in r.iter_lines(chunk_size=64):
    
    if time.time() - last_request > 1: # max 1 request/sec
        real_response = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', params={'screen_name': 'your-id-here', 'count': '1'}, auth=auth)
        text = real_response.json()[0]['text']
       
        print text
        s.write(text[0:90]) # Total cahraters to diaplay 
        last_request = time.time()

