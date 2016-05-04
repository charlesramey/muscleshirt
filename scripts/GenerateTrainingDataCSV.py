import Tkinter, tkFileDialog
from scripts import parse_training_data
from data_analysis import determiner
import os, sys, datetime
import argparse

exercise_dict = {
                 '1': 'bicep curl',
                 '2': 'pushup',
                 '3': 'bench press',
                 '4': 'chest flye',
                 'curl': 'bicep curl',
                 'pushup': 'pushup',
                 'fly': 'chest flye',
                 'press': 'bench press'
                 }

CSV_FILE_NAME = os.getcwd() + "/Training Data " + datetime.datetime.now().strftime("%H-%M") + ".csv"


def main():
    arg_parser = argparse.ArgumentParser(description="Parses for window size, number of features, and whether to use raw data")

    #parse text directory 
    parsed_directory_path = parse_training_data.run()


    num_features = 5
    window_size = 9


    #Gather features for each training file and input into CSV file
    for json_file in os.listdir(parsed_directory_path):
        file_name = os.path.splitext(os.path.basename(json_file))[0]
        exercise_type = file_name.split("_")[0]

        determ = determiner.Determiner(parsed_directory_path + json_file, exercise_dict[exercise_type], num_features)
        determ.extract_features_dict(window_size)
        determ.showPlots(window_size)
        determ.insertFeaturesInCSV(CSV_FILE_NAME)







if __name__ == "__main()__":
    main()


