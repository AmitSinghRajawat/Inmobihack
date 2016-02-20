from config import *
import googlemaps
import traceback
from random import randint

class GoogleAPI(object):
    def __init__(self):
        self.key = GOOGLE_KEY
        self.language = 'en-AU'
        self.client = googlemaps.Client(self.key)
        
        
    def get_nearby_location(self, lat, lng, key="", radius=10,other_param = {}):
        if not lat:
            lat = 12.9667
        if not lng:
            lng = 77.5667
        try:
            location = (lat,lng)
            result = self.client.places(key,location, radius, language=self.language)
        except:
            traceback.print_exc()
            return []
        
        return result['results']
        
    def get_location_list(self, lat_long_dict = {}, favorite = "", distance = 10):
        lat = None
        lng = None
        if not lat_long_dict:
            lat = None
            lng = None 
        
        if distance <=0:
            distance = 10
        
        else:
            lat = float(lat_long_dict['lat'])
            lng = float(lat_long_dict['lng'])
        
        if not favorite:
            favorite = "mess"
        
        result = self.get_nearby_location(lat, lng, favorite, distance)
        if not lat and not lng:
            result = result[0]
        return result
    
    def get_fb_details(self):
        married_status_list = ["married","single"]
        index = randint(0,1)
        selected_married = married_status_list[index]
        office_lat = 12.9667
        office_lng = 77.5667
        likes = [{"name" : "Entertainment", "value" : 20},
                 {"name" : "Novels", "value" : 40},
                 {"name" : "Emeniem", "value" : 50},
                 {"name" : "Discovey Channel", "value" : 40}]
        return selected_married, (office_lat,office_lng), likes
        
    def find_rented_flats(self, lat, lng, radius=10):
        lat_lng = {}
        if lat and lng:
            lat_lng = {}
            lat_lng['lat'] = lat
            lat_lng['lng'] = lng
        return self.get_location_list(lat_lng, favorite = "rent", distance = radius)
    
            
        
