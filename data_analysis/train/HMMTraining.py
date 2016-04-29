import seqlearn

class HMMTrainer(object):
    
    """
    Upon initialization, needs to be given all files in JSON format that correspond to the **ONE** exercise/output that the HMM is being trained for 
    @param [training_files]: The list of file paths that contain the feature data for the HMM outputs
    """
    def __init__(self, training_files):
        self.training_files = []


    def train(self):
        if not self.training_files:
            self.training_files = self._askForTrainingFiles()

        #For each training file, parse the file to extract the dictionary of keys (feature names) and feature lists (values)
        






    def _askForTrainingFiles(self):
        import Tkinter, tkFileDialog
        files = list(tkFileDialog.askopenfilenames(title = "Choose Training Files For HMM", filetypes = [("Sensor List JSON", ".json" )]))

        if not len(files) > 0: 
            raise ValueError("No files chosen")

        return files








def main():

    ##testing code trying to figure out wtf seqlearn needs as input
    import numpy as np
    text = [w.split() for w in ["this DT",
	                            "is DT",
	                            "a DT",
	                            "test DT",
	                            "for DT",
	                            "a DT",
	                            "hidden DT",
	                            "Markov N",
	                            "model N"]]
    words, y = zip(*text)
    lengths = [len(text)]
    
    vocab, identities = np.unique(words, return_inverse=True)
    X = (identities.reshape(-1, 1) == np.arange(len(vocab))).astype(int)
    n_features = X.shape[1]
    print "done"









if __name__ == "__main__":
    main()




