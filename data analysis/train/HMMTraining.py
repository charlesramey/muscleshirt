import seqlearn

class HMMTrainer(object):
    
    """
    Upon initialization, needs to be given all files in JSON format that correspond to the **ONE** exercise/output that the HMM is being trained for 
    @param training_files: The list of file paths that contain the feature data for the HMM outputs
    """
    def __init__(self, training_files):
        self.training_files = []












if __name__ == "__main__":
    import Tkinter, tkFileDialog
    root = Tkinter.Tk()
    files = list(tkFileDialog.askopenfiles(parent = root, title = "Choose Training Files"))
    print files




