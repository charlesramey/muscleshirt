import sys
import json
import scipy.signal as sig

class Determiner(object):

    """
    Sample file should point to a json list file that contains the keys corresponding to sensor values, plus the values in a single array for the time capture period. 
    """
    def __init__(self, json_list_file):
        self.json_file = json_list_file
        self.smoothed_data = None

        with open(self.json_file) as f:
            self.values_dict = json.load(f)

        self.num_features = 5



    def get_smoothed_data(self):
        if self.smoothed_data: return self.smoothed_data

        self.smoothed_data = {}
        for key in self.values_dict:
            self.smoothed_data[key] = self._smooth(self.values_dict[key])

        return self.smoothed_data




    def _smooth(self, list):
        window_length = 11     #!!!!must be odd!!!!
        poly_order = 7    #Polynomial order of the data

        return sig.savgol_filter(list, window_length, poly_order)
        



    def determine(self, num_values):
    	pass



    def findEMGActivationLevels(self):
    	keys = ['emg_chest', 'emg_upper_arm', 'emg_forearm']
    	MAX_VALUE_THRESHOLD = .5

    	num_max_vals = {}
    	for k in keys:
    		emg_arr = self.values_dict[k]
    		max_values_present = [x for x in emg_arr if x >= max(emg_arr) * MAX_VALUE_THRESHOLD]
    		num_max_vals[k] = len(max_values_present)


    	return num_max_vals





def main():
    import sys, os
    import matplotlib.pyplot as plt

    json_file = "./training data/parsed/1_3_list.json"
    fname = json_file.split(".json")[0].split("/")[-1]
    d = Determiner(json_file)

    smoothed_data = d.get_smoothed_data()

    for i, k in enumerate(d.values_dict):
        plt.plot(d.values_dict[k], color="b")
        plt.plot(smoothed_data[k], color="r")
        plt.title(fname + ": " + k)
        plt.savefig("./figures/"+ fname + "-" + k + ".png")
        plt.close("all")

    print d.findEMGActivationLevels()


if __name__ == "__main__":
    main()

