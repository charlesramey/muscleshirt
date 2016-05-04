
"""
Given a txt file that contains data in the original format, return a dictionary whose keys are the data keys and contain list of values.
@param file: The file path with the training data
@return A dict with keys that name the lists of data
"""
import tkFileDialog





BLOCK_SPACING = 6		#number of lines between consecutive entries in a block

def create_lists(file):
	values_dict = {"pitch_forearm": [], 
	"roll_forearm": [],
	"pitch_upper_arm": [],
	"roll_upper_arm": [], 
	"emg_chest": [], 
	"emg_upper_arm": [], 
	"emg_forearm": [] }


	with open(file, "rb") as f: 
		data = [x.rstrip() for x in f.readlines()]
		
	beg_block_pointer = 0
	while(beg_block_pointer + BLOCK_SPACING < len(data)):
		#extract values

		pitch_forearm_val, roll_forearm_val = getPitchAndRoll(data[beg_block_pointer + 1])
		pitch_forearm_val, roll_forearm_val = (float(pitch_forearm_val), float(roll_forearm_val))

		pitch_upper_arm_val, roll_upper_arm_val = getPitchAndRoll(data[beg_block_pointer + 0])
		pitch_upper_arm_val, roll_upper_arm_val = (float(pitch_upper_arm_val), float(roll_upper_arm_val))

		emg_chest_val = int(data[beg_block_pointer + 2])
		emg_upper_arm_val = int(data[beg_block_pointer + 3])
		emg_forearm_val = int(data[beg_block_pointer + 4])

		#add values to dict
		values_dict['pitch_forearm'].append(pitch_forearm_val)
		values_dict['roll_forearm'].append(roll_forearm_val)
		values_dict['pitch_upper_arm'].append(pitch_upper_arm_val)
		values_dict['roll_upper_arm'].append(roll_upper_arm_val)
		values_dict['emg_chest'].append(emg_chest_val)
		values_dict['emg_upper_arm'].append(emg_upper_arm_val)
		values_dict['emg_forearm'].append(emg_forearm_val)

		#go to next block
		beg_block_pointer += BLOCK_SPACING


	return values_dict




def getPitchAndRoll(line):
	data = line.split(": ")[1]
	data_arr = data.split(", ")

	return tuple(data_arr)


"""
Parses the training data and then returns the directory path of the parsed data
"""
def run():
    import os, json, Tkinter, tkFileDialog
    root = Tkinter.Tk()

    os.chdir(tkFileDialog.askdirectory(title="Choose Training Data TEXT Files Directory"))

    if not os.path.exists(os.getcwd() + "/parsed/"):
        os.makedirs(os.getcwd() + "/parsed/")

    files = [x for x in os.listdir(os.getcwd()) if os.path.isfile(x) and ".txt" in x]	#exclude source file
    print files

    for f_name in files:
        try:
            values_dict = create_lists(f_name)

            name = os.path.splitext(os.path.basename(f_name))[0]
            with open("./parsed/" + name + "_list.json", "w+") as f:
                f.write(json.dumps(values_dict, indent=4))

        except Exception, e:
            import traceback
            print "ERROR IN FILE: " + f_name
            print traceback.print_exc()



    root.destroy()

    return os.getcwd() + "/parsed/"


def main():
    run()






if __name__ == "__main__":
    main()