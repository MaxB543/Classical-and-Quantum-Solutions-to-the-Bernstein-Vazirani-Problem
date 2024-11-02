# This script is responsable for writing qunatum test results 

import os
import csv

import matplotlib
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit

FOLDER = "results"
SUB_FOLDER = "secrets"
TXT_FILE = "results"    # Stores a log of all tests and results 
QC_FILE = "qc"         # latex code and svg for undtraspiled circuit
HIST_FIG = "hist"   # svg for result histrogram
CSV_FILE ="results"     # CSV contining all results for jobs with a certian size

# Contains important info for a given test result
class ResultData:
    def __init__(self, backend:str, secret:str, shots:int, counts=None, qc:QuantumCircuit=None, tqc:QuantumCircuit=None, id:str="", tag:str=""):
        self.backend = backend
        self.secret = secret
        self.shots = shots
        self.counts = counts
        self.qc = qc
        self.tqc = tqc
        self.id = id
        self.tag = tag
    
    def secret_len(self):
        return len(self.secret)
    
    # Find success rate 
    def accuracy(self):
        if self.secret in self.counts.keys():
            return self.counts[self.secret]/self.shots
        else:
            return 0.0


# Save the given result to a text file
def save_result(result:ResultData):

    # make a result folder if it does not yet exist
    if not os.path.isdir(FOLDER):
        os.mkdir(FOLDER)

    if not result.counts == None:
        write_to_hist(result)
        write_to_csv(result)
        write_to_gen_csv(result)
    if not result.qc == None:
        write_qc(result)

# Depricated and not used 
def write_to_txt(result:ResultData):
    filename = os.path.join(FOLDER, TXT_FILE)+".txt"
    mode = "a"
    if not os.path.exists(filename):
        mode = "w"
    with open(filename, mode=mode, newline="") as file:
        file.write("Backend: " + result.backend + " with secret " + result.secret + " has accuracy " + str(result.accuracy())+"\n")
        file.close()

# Write results to csv containing backen, secret and frequncy of all classical outputs
def write_to_csv(result:ResultData, id:str=None):
    if result.backend == "basic_simulator":
        return # There is no point in writng perfectly accuate results to csv
    n = result.secret_len()
    f = CSV_FILE + "_" + str(n) + ".csv"
    if not id == None:
        f = id + "_" + f
    filename = os.path.join(FOLDER, f)
    if not os.path.exists(filename):
        with open(filename, mode='w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            header = ["backend", "secret", "accuracy"]
            header = header + get_bins(n)           
            writer.writerow(header)

            file.close()

    with open(filename, mode='a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        bins = get_bins(n)
        # Write the data row
        line = [result.backend, '0b'+result.secret, result.accuracy()]
        for bin in bins:
            if bin in result.counts.keys():
                line.append(result.counts[bin]/result.shots)
            else:
                line.append(0.0)
        writer.writerow(line)
        file.close()

# Write to csv contining backend, secret, accurcy, secret lenght and job tag, if any
def write_to_gen_csv(result:ResultData):
    if result.backend == "basic_simulator":
        return # There is no point in writng perfectly accuate results to csv
    n = result.secret_len()
    f = CSV_FILE + "_accuracy.csv"

    filename = os.path.join(FOLDER, f)
    if not os.path.exists(filename):
        with open(filename, mode='w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            header = ["backend", "secret", "accuracy", "size","tag"]        
            writer.writerow(header)

            file.close()

    with open(filename, mode='a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # Write the data row
        line = [result.backend, '0b'+result.secret, result.accuracy(), result.secret_len(), result.tag]
        writer.writerow(line)
        file.close()

# Print a histogram for circuit outputs
def write_to_hist(result:ResultData):
    if result.secret_len() > 6:
        # There is no point in printing a histogram of this size
        return
    f = result.backend + "_" + HIST_FIG + ".png"
    filename = os.path.join(get_job_folder(result.secret), f)
    if os.path.isfile(filename):
        filename = os.path.join(get_job_folder(result.secret), result.backend + "_" + result.id + "_" + HIST_FIG + ".png")
    sim_hist = plot_histogram(result.counts)
    sim_hist.savefig(filename)
    matplotlib.pyplot.close()

# Retruns a folter to save job in (based on secret)
def get_job_folder(secret:str)->str:
    sub_dir = "secret_" + secret
    dir = os.path.join(FOLDER, SUB_FOLDER, sub_dir)

    # Make foleder if it does not yet exist
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir

# makes a list of all possible binary outputs for the given qc size to be used in csv    
def get_bins(n:int):
    arr=[]
    l = 2**n
    for i in range(l):
        arr.append(bin(i)[2:].zfill(n))

    return arr

# Writes result's quntum circuit to a .tex file and .png to be viewed later
def write_qc(result:ResultData):
    f = QC_FILE
    filename = os.path.join(get_job_folder(result.secret), f)
    if not result.qc == None and not os.path.isfile(filename+".tex"):
        result.qc.draw('latex_source', filename=(filename+".tex"))
        result.qc.draw(output = 'mpl', filename=(filename+".png"))
    if not result.tqc == None:
        if os.path.isfile(filename+"_transpiled("+result.backend+").tex"):
            filename = filename + "_" + result.id
        result.tqc.draw('latex_source', filename=(filename+"_transpiled("+result.backend+").tex"))