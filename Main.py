'''

    Server re use
    https://stackoverflow.com/questions/12362542/python-server-only-one-usage-of-each-socket-address-is-normally-permitted
    
    http://flask.pocoo.org/snippets/116/
    https://www.w3schools.com/html/html5_serversentevents.asp

'''
# 
# Make sure your gevent version is >= 1.0

import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
import random
from flask import request
from flask_cors import CORS
from flask import Flask, Response
import requests
import os
import sys

import time

def get_random_int(start, end):
    return random.randint(start, end)

# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.items() if k]
        
        return "%s\n\n" % "\n".join(lines)

app = Flask(__name__)
CORS(app) #this will enable all (free - world)
subscriptions = []

# Client code consumes like this.
@app.route("/")
def index():
    debug_template = """
     <html>
       <head>
       </head>
       <body>
         <h1>Cricket Updates</h1>
         <div id="event"></div>
         <script type="text/javascript">

         var eventOutputContainer = document.getElementById("event");
         var evtSrc = new EventSource("/subscribe");

         evtSrc.onmessage = function(e) {
             console.log(e.data);
             eventOutputContainer.innerHTML += e.data + '<br>';
         };

         </script>
       </body>
     </html>
    """
    return(debug_template)

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

'''
    http://localhost:5000/publish?message=one
'''
@app.route("/publish")
def publish():
    
    message  = request.args.get('message')
    
    #print('me : '+message)
    
    #Dummy data - pick up from request for real data
    def notify():
        
        for sub in subscriptions[:]:
            sub.put(message)
    
    gevent.spawn(notify)    
    
    return "OK"

@app.route("/update")
def update_events():
    
    #return "OK"
    
    for x in range(5):
        url = 'http://localhost:5000/publish'
    
        response = requests.get(url)        
        print(response)
        print(url)
    
    return "OK"

@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    
    
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish
    
    
    '''
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host= host, port = port, use_reloader = False)
    '''