from __future__ import division
import operator
import math
from googleMapAPI import api,config
maps = api.GoogleAPI()
MIN_OFFSET = 3 # kms
MAX_OFFSET = 10 # kms
MIN = 0
MAX = 100
factor = math.pi/180.0

def get_best_location(preference_list=list(),selected_married = "",office_lat = "",office_lng = "",likes = ""):
	fb_profile = (selected_married,(office_lat,office_lng),likes)
	preference_list = fb_profile[2]
	preference_list.extend(config.STATUS_DICT[fb_profile[0]])

	location_dict = dict()
	center_obj = get_center_obj(preference_list)
	preference_list.remove(center_obj)
	center_position = {'lat':fb_profile[1][0],'lng':fb_profile[1][1]}

	sortedlist = sorted(preference_list, key=operator.itemgetter('value'),reverse=True)
	for obj in sortedlist:
		val = MAX - obj.get('value')
		distance = get_distance(val)
		print distance
		raw_data = maps.get_location_list(center_position,obj['name'],distance) # expecting list format
		location_dict[obj['name']] = refine_position(raw_data)
		location_dict[obj['name']]['weight'] = obj.get('value')
	print raw_data
	location_dict,total_weight = get_radians(location_dict)
	location_dict = x_y_z(location_dict)
	xyz_dict = cumulative_points(location_dict,total_weight)
	final_dict = mid_point(xyz_dict)
	flats_list = maps.find_rented_flats(final_dict['lat'],final_dict['lng'])
	relevant_results_dict = dict()
	relevant_results_dict['flats_list'] = flats_list
	relevant_results_dict['nearby_locations'] = location_dict
	return relevant_results_dict

def x_y_z(location_dict):
	for key,val in location_dict.items():
		location_dict[key]['x'] = math.cos(location_dict[key]['lat_rad']) * math.cos(location_dict[key]['lng_rad'])
		location_dict[key]['y'] = math.cos(location_dict[key]['lat_rad']) * math.sin(location_dict[key]['lng_rad'])
		location_dict[key]['z'] = math.sin(location_dict[key]['lat_rad'])
	return location_dict

def cumulative_points(location_dict,total_weight):
	x_y_z_dict = dict()
	x_y_z_dict['x'] = 0
	x_y_z_dict['y'] = 0
	x_y_z_dict['z'] = 0
	for key,val in location_dict.items():
		x_y_z_dict['x'] += location_dict[key]['x']*location_dict[key]['weight']
		x_y_z_dict['y'] += location_dict[key]['y']*location_dict[key]['weight']
		x_y_z_dict['z'] += location_dict[key]['z']*location_dict[key]['weight']
	x_y_z_dict['x'] = location_dict[key]['x']/total_weight
	x_y_z_dict['y'] = location_dict[key]['y']/total_weight
	x_y_z_dict['z'] = location_dict[key]['z']/total_weight
	return x_y_z_dict

def mid_point(x_y_z_dict):
	mid_point_dict = dict()
	final_result = dict()
	mid_point_dict['lon'] = math.atan2(x_y_z_dict['y'],x_y_z_dict['x'])
	mid_point_dict['hyp'] = math.sqrt(x_y_z_dict['x']*x_y_z_dict['x']+x_y_z_dict['y']*x_y_z_dict['y'])
	mid_point_dict['lat'] = math.atan2(x_y_z_dict['z'],mid_point_dict['hyp'])
	final_result['lat'] = mid_point_dict['lat']/factor
	final_result['lng'] = mid_point_dict['lon']/factor
	return final_result

def refine_position(raw_data):
	for data in raw_data[:1]:
		data['lat'] = data['geometry']['location']['lat']
		data['lng'] = data['geometry']['location']['lng']
	return data

def get_radians(location_dict):
	total_weight = 0
	for key,val in location_dict.items():
		location_dict[key]['lat_rad'] = (location_dict[key]['lat'])*factor
		location_dict[key]['lng_rad'] = (location_dict[key]['lng'])*factor
		total_weight += location_dict[key]['weight']
	#location_dict['total_weight'] = total_weight
	return location_dict,total_weight

def get_distance(value):
	distance = MIN_OFFSET + ((MAX_OFFSET-MIN_OFFSET)/MAX)*value
	return distance

def get_center_obj(p_obj):
	max_ = -1
	for obj in p_obj:
		if max_ < obj.get('value'):
			ret = obj
			max_ = obj.get('value')
	return ret

if __name__=='__main__':
	preference_list = list()
	get_best_location(preference_list)
