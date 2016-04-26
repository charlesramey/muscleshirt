import json 
import matplotlib
import numpy as np 
import scipy.ndimage
import peakutils

def smooth(data):
	filtered = scipy.ndimage.filters.gaussian_filter(data, 0)
	return filtered
def find_peaks(data):
	peaks = peakutils.indexes(data, thres=0.02/max(data), min_dist=4)
	return peaks
