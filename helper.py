import json
from googleMapAPI import api,config
maps = api.GoogleAPI()


def parse_fb_data(json_data):
    data = json.loads(json_data)
    final_data = {}
    if not data['relationship_status']:
        final_data['relationship_status'] = 'single'
    else:
        final_data['relationship_status'] = data['relationship_status']
    
    final_data['current_location_lat'] = data['latitude']
    final_data['current_location_lng'] = data['longitude']
    final_data['name'] = data['name']
    final_data['age'] = data['age_range']['min']
    current_company_name = '' 
    if not data['work']:
        current_company_name = data['work'][0]['employer']['name']
        rev_geocode = maps.get_city_name(float(final_data['current_location_lat']),float(final_data['current_location_lng']))
        find_lat_long = current_company_name + " " + rev_geocode
        lat,lng = maps.get_lat_lng(find_lat_long)
        final_data['work_lat'] = lat
        final_data['work_lng'] = lng
    company_name = str(data['work'][0]['employer']['name']) + " "  +  str(data['work'][0]['location']['name'])
    lat,lng = maps.get_lat_lng(company_name)
    final_data['work_lat'] = lat
    final_data['work_lng'] = lng
    final_data['work'] = data['work'][0]
    final_data['likes'] = data['likes']['data'][:3]
    return final_data