from flask import Flask,request
from helper import *
from googleMapAPI import api,config
maps = api.GoogleAPI()
from analytics import *
import copy
from flask import Response, json

class Orchestrator(object):
    def __init__(self):
        self.user = None

    def handle_fb_data(self,json_data):
        data = parse_fb_data(json_data)
        print data
        likes = [{"name" : "Office", "value" : 50},
                 {"name" : "Bar", "value" : 30},
                 {"name" : "Sport", "value" : 40},
                 {"name" : "Discovey Channel", "value" : 40}]
        
        result = get_best_location(selected_married=data['relationship_status'], office_lat = data['work_lat'],office_lng = data['work_lng'],
                          likes = likes)
        json_data = result
        new_dic = {}
        new_dic['flats_list'] = []
        new_dic['nearby_locations'] = {}
        for element in json_data['flats_list']:
            new_dic['flats_list'].append(element)
        new_dic['nearby_locations'] = json_data['nearby_locations']
        new_dic['office_lat'] = json_data['office_lat']
        new_dic['office_lng'] = json_data['office_lng']
        #test = json.dumps(new_dic)
        return new_dic
    
    def handle_second_call(self,json_data):
        data = json.loads(json_data)
        lat = float(data['lat'])
        lng = float(data['lng'])
        likes = [{"name" : "Entertainment", "value" : 50},
                 {"name" : "Novels", "value" : 20},
                 {"name" : "Emeniem", "value" : 70},
                 {"name" : "Discovey Channel", "value" : 60}]
        likes_lis = data['weight']
        lis_nw = []
        
        for key,value in likes_lis.items():
            lis_nw.append({'name':key,'value':value})
    
        result = get_best_location(office_lat = lat,office_lng = lng,
                          likes = lis_nw)
        return result

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
    return Response(json.dumps(output),  mimetype='application/json')

@app.route('/updateDetails',methods = ['POST'])
def second_call():
    json_data = request.get_data()
    print json_data
    output = orchestrator.handle_second_call(json_data)
    return Response(json.dumps(output),  mimetype='application/json')


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)