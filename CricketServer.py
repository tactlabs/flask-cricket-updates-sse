# author: oskar.blom@gmail.com
# http://flask.pocoo.org/snippets/116/
# Make sure your gevent version is >= 1.0
import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
import requests
import random

from flask import Flask, Response

import time

def get_random_int(start, end):
    return random.randint(start, end)

app = Flask(__name__)

def call_publish_api(msg):
    url = 'http://localhost:5000/publish?message='+msg    
    response = requests.get(url)

@app.route("/update")
def update_events():
    
    overs_max = 2  
    teams = ["India", "England"]
    current_player = "Sachin" 
    team_1_score = 0
    team_2_score = 0
    
    for innings in range(2):
        
        call_publish_api(teams[innings]+" batting :")
    
        for over in range(overs_max):
            
            call_publish_api("Over "+str(over+1)+":")
            
            time.sleep(1)
            
            for x in range(6):
                
                runs = get_random_int(0, 6)
                
                team_1_score = team_1_score + runs
                
                call_publish_api("Ball "+str(x+1)+": "+current_player+" scored "+str(runs)+" runs")    
                
                time.sleep(2)
            
        call_publish_api("Final Score :  "+str(team_1_score))        
    
    return "OK"


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5001), app)
    server.serve_forever()
    
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish