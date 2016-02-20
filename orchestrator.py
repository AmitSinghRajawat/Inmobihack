from flask import Flask,request
import json

class Orchestrator(object):
    def __init__(self):
        self.user = None
    
    
    def handle_user(self,user):
        json_data = {"status" : "Success"}
        return json.dumps(json_data)

orchestrator = Orchestrator()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/fbInfo',methods = ['POST'])
def user():
    json_data = request.get_data()
    print(json_data)
    output = orchestrator.handle_user(json_data)
    return output


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)