'''

    CORS
    https://flask-cors.readthedocs.io/en/latest/
'''
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

def call_publisher_api(msg):
    url = 'http://localhost:5000/publish?message='+msg    
    response = requests.get(url)

@app.route("/update")
def update_events():
    
    overs_max = 2  
    ball_max_per_over = 3
    teams = ["India", "England"]
    teams_score = [0, 0]
    team_1_player = "Sachin"
    team_1_player = "Paul" 
    current_player = ""
    
    
    for innings in range(2):
        
        call_publisher_api(teams[innings]+" batting :")
    
        for over in range(overs_max):
            
            call_publisher_api("Over "+str(over+1)+":")
            
            time.sleep(1)
            
            for x in range(ball_max_per_over):
                
                runs = get_random_int(0, 6)
                
                teams_score[innings] = teams_score[innings]+runs 
                
                call_publisher_api("Ball "+str(x+1)+": "+current_player+" scored "+str(runs)+" runs")    
                
                time.sleep(get_random_int(1, 4))
            
        call_publisher_api(teams[innings]+" Final Score :  "+str(teams_score[innings]))
        
    time.sleep(1)            
    
    if(teams_score[0] > teams_score[1]):
        call_publisher_api("<br>"+teams[0]+" wins by "+str((teams_score[0] - teams_score[1]))+ " runs")
    elif(teams_score[0] < teams_score[1]):    
        call_publisher_api("<br>"+teams[1]+" wins by 10 wickets")
    else:
        call_publisher_api("<br> Match Draw")
    
    return "OK"


if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5001), app)
    server.serve_forever()
    
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish