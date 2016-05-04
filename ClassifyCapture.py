from scripts import parse_training_data as parse
from data_analysis import determiner as det
from network import AzureClassificationRequest as req
import sys, os, json


TEMP_JSON_FNAME = "./temp.json"
DEFAULT_WINDOW_SIZE = 5







"""
Given a text capture file, outputs the classification obtained through Azure
"""
def run(file):
    vals_dict = parse.create_lists(file)
    
    #create temp JSON file
    with open(TEMP_JSON_FNAME, "w+") as json_data_fp:
        json_data_fp.write(json.dumps(vals_dict, indent = 4))

    #get features
    feature_extractor = det.Determiner(TEMP_JSON_FNAME)
    features_dict = feature_extractor.extract_features_dict(DEFAULT_WINDOW_SIZE)
    feature_extractor.showPlots()

    #send features for classification 
    result = json.loads(req.sendRequest(features_dict))
    print "=======================\nResults:\n=======================\n"
    col_names = result['Results']['Web Output']['value']['ColumnNames']
    col_vals = result['Results']['Web Output']['value']['Values'][0]

    for i,name in enumerate(col_names[:-1]):
        print name + ":\t" + col_vals[i]

    print "\n\n\nBest Prediction\n------------------------\n"
    print "Exercise: %s\t\tProbability: %0.3f\n\n" % (col_vals[-1].title(), float(max(col_vals[:-1])))


    #remove temp JSON file
    os.remove(TEMP_JSON_FNAME)



def main():
    if len(sys.argv) > 1:
        text_capture_file = sys.argv[1]

    else:
        text_capture_file =  "./training data/1_1.txt"


    run(text_capture_file)



if __name__ == "__main__":
    main()