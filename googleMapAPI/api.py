from config import *
import googlemaps
import traceback

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
        else:
            lat = float(lat_long_dict['lat'])
            lng = float(lat_long_dict['lng'])
        
        if not favorite:
            favorite = "mess"
        
        result = self.get_nearby_location(lat, lng, favorite, distance)
        return result
    
        
