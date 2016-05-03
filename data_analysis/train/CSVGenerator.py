import csv
SENSOR_NUM_FEATURES = 5
HEADER_ROWS = [
               "_excercise",         #this row indicates what exercise is being performed (for training data). For real time samples (prediction), leave this field as None 
               "emg_forearm_1", "emg_forearm_2", "emg_forearm_3", "emg_forearm_4", "emg_forearm_5", 
               "emg_upper_arm_1", "emg_upper_arm_2", "emg_upper_arm_3", "emg_upper_arm_4", "emg_upper_arm_5",
               "emg_chest_1", "emg_chest_2", "emg_chest_3", "emg_chest_4", "emg_chest_5",
               "pitch_forearm_1", "pitch_forearm_2", "pitch_forearm_3", "pitch_forearm_4", "pitch_forearm_5",
               "roll_forearm_1", "roll_forearm_2", "roll_forearm_3", "roll_forearm_4", "roll_forearm_5",
               "pitch_upper_arm_1", "pitch_upper_arm_2", "pitch_upper_arm_3", "pitch_upper_arm_4", "pitch_upper_arm_5",
               "roll_upper_arm_1", "roll_upper_arm_2", "roll_upper_arm_3", "roll_upper_arm_4", "roll_upper_arm_5",
               ]

class CSVGenerator(object):
    """
    Provides an easy interface for creating CSV training files for Azure ML
    """

    """
    Inserts data from a list of dictionaries containing the column names (dict keys) and values (dict key values) 
    @param csv_file_path: File path to CSV File to be written. Either existing or new. Will be opened in file format 'a+b'
    @param data_dicts_list: A LIST of dictionaries, each containing all values of HEADER_ROWS as keys and values for each 
    """
    @staticmethod
    def insertData(csv_file_path, data_dicts_list):
        with open(csv_file_path, "a+b") as csv_file:
            dr = csv.DictReader(csv_file)
            headers = dr.fieldnames

            #if headers and not len(set(headers).intersection(HEADER_ROWS)) == len(HEADER_ROWS):
                #raise ValueError("Present header values are not the same as HEADER_ROWS. Check CSVGenerator.py for expected header row values and " + csv_file_path + " for input header values")

            if not headers: 
                headers = sorted(data_dicts_list[0].keys())


            dw = csv.DictWriter(csv_file, headers)

            dw.writeheader()
            dw.writerows(data_dicts_list)










def main():
    import random
    list = []
    for i in range(5):
        test = {}
        for x in HEADER_ROWS:
            if x is "excercise":
                test[x] = None
                continue

            test[x] = random.randint(0,100)
        
        list.append(test)

    CSVGenerator.insertData("test.csv", list)












if __name__ == "__main__":
    main()


