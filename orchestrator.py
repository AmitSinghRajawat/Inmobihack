from flask import Flask,request
import json
from helper import *
from googleMapAPI import api,config
maps = api.GoogleAPI()
from analytics import *

class Orchestrator(object):
    def __init__(self):
        self.user = None

    def handle_fb_data(self,json_data):
        data = parse_fb_data(json_data)
        print data
        likes = [{"name" : "Entertainment", "value" : 20},
                 {"name" : "Novels", "value" : 40},
                 {"name" : "Emeniem", "value" : 50},
                 {"name" : "Discovey Channel", "value" : 40}]
        
        result = get_best_location(selected_married=data['relationship_status'], office_lat = data['work_lat'],office_lng = data['work_lng'],
                          likes = likes)
        json_data = result
        return json.dumps(json_data)

orchestrator = Orchestrator()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/fbInfo',methods = ['POST'])
def fb():
    json_data = request.get_data()
    print(json_data)
    output = orchestrator.handle_fb_data(json_data)
    return output


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)