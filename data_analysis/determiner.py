import sys
import json
import scipy.signal as sig
import matplotlib.pyplot as plt

class Determiner(object):

    """
    Sample file should point to a json list file that contains the keys corresponding to sensor values, plus the values in a single array for the time capture period. 
    """
    def __init__(self, json_list_file, exercise = None, num_features_per_sensor = 5):
        self.json_file = json_list_file
        self.smoothed_data = None

        with open(self.json_file) as f:
            self.values_dict = json.load(f)

        if num_features_per_sensor % 2 == 1:
            self.num_features = num_features_per_sensor
        else:
            raise ValueError("Features per sensor must be odd!")

        
        self.feature_indices = []
        self.freeze_frame_info = (None, None, None)
        self.features_dict = {'_exercise': exercise}




    def insertFeaturesInCSV(self, csv_file_path):
        from data_analysis.train import CSVGenerator as gen
        gen.CSVGenerator.insertData(csv_file_path, [self.extract_features_dict()])



    """
    Extracts a dictionary of features for insertion into an excel spreadsheet using the CSV Generator
    @param window_size: An ODD integer indicating the window width to sweep the data curve. 
    """
    def extract_features_dict(self, window_size = 5, use_preprocessed = True):
        if window_size < self.num_features: raise ValueError("Window size cannot be less than the number of features")

        if len(self.features_dict.keys()) > 1:
            return self.features_dict

        data_dict = self.preprocess_data() if use_preprocessed else self.values_dict
        
        name, indx, max_val = self._find_freeze_frame_info(data_dict, window_size)
        print "Using freeze frame based on *** %s *** with max value: %f at index %d" % (name, max_val, indx)
        features_indices = self._get_feature_indices(indx, window_size)

        features_dict = {}
        for k in data_dict:
            data = list(data_dict[k])
            for i,feature_ind in enumerate(features_indices):
                features_dict[k + "_" + str(i+1)] = data[feature_ind]
        


        self.features_dict.update(features_dict)
        return self.features_dict




    def preprocess_data(self):
        return self._get_smoothed_data()








    def showPlots(self):
        preprocessed_data = self.preprocess_data()
        feature_indices = self.feature_indices
        _, indx, max_val = self.freeze_frame_info

        for k in [x for x in preprocessed_data]:  #only consider emg readings
            data = preprocessed_data[k]
            plt.figure(k)
            plt.title(k)
            plt.plot(self.values_dict[k], color ="red")
            plt.plot(data, color="green", linewidth=3)
            plt.plot(indx, max_val, "bv", markersize=10)
            plt.plot(feature_indices, [data[x] for x in feature_indices], "yo", markersize=5)
            
        plt.show()







    def _find_freeze_frame_info(self, data_dict, window_size):
        val_list = []
        for k in [x for x in data_dict if "emg" in x]:  #only consider emg readings
            data = list(data_dict[k])
            span_lim = int(round(window_size/2.0))     #we must not find a max before/after this index in the data for beginning/end
            max_val = max(data[span_lim-1:-span_lim])
            ind = data.index(max_val)      #finds the first index of the max value between span_lim and len - span_lim
            val_list.append((k, ind, max_val))

        name, indx, valz = max(val_list, key = lambda x: x[2])

        print "Max value of %f found for %s at index %d" % (valz, name, indx)
       
        self.freeze_frame_info = (name, indx, valz)
        return (name, indx, valz)   #return only index of max tuple







    """
    Given an index and window size, finds the feature data points 
  
    @param index: The index of the max value 
    @param window_size: The window size to use for finding features
    @returns [indices]: A list of feature indices
    """
    def _get_feature_indices(self, index, window_size):
        import math
        span_lim = window_size/2

        step_val = int( math.ceil(float(window_size)/(self.num_features)) )
        feature_indices = range(index-span_lim, index+span_lim+1, step_val)
        #feature_indices = [index-span_lim, index+span_lim] + range(index+step_val, index+span_lim, step_val)

        self.feature_indices = sorted(feature_indices)
        return sorted(feature_indices)







    def _get_smoothed_data(self):
        if self.smoothed_data: return self.smoothed_data

        self.smoothed_data = {}
        for key in self.values_dict:
            self.smoothed_data[key] = self._smooth(self.values_dict[key])

        return self.smoothed_data




    def _smooth(self, list):
        window_length = 11     #!!!!must be odd!!!!
        poly_order = 7    #Polynomial order of the data

        return sig.savgol_filter(list, window_length, poly_order)
        




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

    json_file = "./training data/parsed/3_8_list.json"
    fname = json_file.split(".json")[0].split("/")[-1]
    d = Determiner(json_file)

    d.insertFeaturesInCSV("C:/Users/navee/Desktop/test.csv")

 


if __name__ == "__main__":
    main()

