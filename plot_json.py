import json 
import matplotlib
import numpy as np 
import scipy
import peakutils

class graph_tools(object):

	def smooth(data):
		return scipy.ndimage.filters.gaussian_filter(data, 0)

	def find_peaks(data)
		return peakutils.indexes(data, thres=0.02/max(data), min_dist=5)