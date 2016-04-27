import sys
import json

class Determiner(object):

	"""
	Sample file should point to a json list file that contains the keys corresponding to sensor values, plus the values in a single array for the time capture period. 
	"""
	def __init__(self, json_list_file):
		self.json_list_file = json_list_file

		with open(self.json_list_file) as f:
			self.values_dict = json.load(f)


	def determine(self):
		pass



	def findEMGActivationLevels(self):
		keys = ['emg_chest', 'emg_upper_arm', 'emg_forearm']
		MAX_VALUE_THRESHOLD = .5

		num_max_vals = {}
		for k in keys:
			emg_arr = self.values_dict[k]
			max_values_present = [x for x in emg_arr if x >= max(emg_arr)*MAX_VALUE_THRESHOLD]
			num_max_vals[k] = len(max_values_present)


		return num_max_vals




if __name__ == "__main__":
	import sys

	json_file = sys.argv[1]
	d = Determiner(json_file)
	print d.findEMGActivationLevels()
	

