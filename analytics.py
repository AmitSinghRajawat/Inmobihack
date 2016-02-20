from __future__ import division
import operator
MIN_OFFSET = 3 # kms
MAX_OFFSET = 10 # kms
MIN = 0
MAX = 100 
def get_best_location(preference_list=list()):
	import pdb;pdb.set_trace()
	location_dict = dict()
	center_obj = get_center_obj(preference_list)
	preference_list.append({'name':'home','value':center_obj['value']})
	preference_list.remove(center_obj)
	import pdb;pdb.set_trace()
	center_obj = get_locations(dict(),center_obj['name'],0)

	sortedlist = sorted(preference_list, key=operator.itemgetter('value'),reverse=True)
	for obj in preference_list:
		val = MAX - obj.get('value')
		distance = get_distance(val)
		print distance
		location_dict[obj['name']] = get_locations(center_obj,obj['name'],distance) # expecting list format
	print location_dict
	# I have got all the locations of every preference
	

def get_distance(value):
	distance = MIN_OFFSET + ((MAX_OFFSET-MIN_OFFSET)/MAX)*value
	return distance

def get_locations(center_obj=dict(),category=str(),distance=float()):
	return [1,2,3,4,5]

def get_center_obj(p_obj):
	max_ = -1
	for obj in p_obj:
		if max_ < obj.get('value'):
			ret = obj
			max_ = obj.get('value')
	return ret

if __name__=='__main__':
	#center_obj = {'latitude':11.81836730000000000000,'longitude':79.78678120000000000000,'value':90}
	preference_list = list()
	preference_list.append({'name':'office','value':100})
	preference_list.append({'name':'sports','value':50})
	preference_list.append({'name':'pubs','value':20})
	get_best_location(preference_list)
