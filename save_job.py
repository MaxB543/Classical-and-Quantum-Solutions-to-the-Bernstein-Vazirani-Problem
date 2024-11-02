# Script use to save and load job id to Retrieve past qiskit jobs from IBM quantum computers 

import os

JOB_FOLDER = ".qiskit_jobs"
JOB_TXT = "jobs.txt"

# Class used to store useful Job info
class JobData:
    def __init__(self, job_id:str, backend:str, secret:str, shots:int, tag=""):
        self.job_id = job_id
        self.backend = backend
        self.secret = secret
        self.shots = shots
        self.tag = tag

# Save qiksit job data so that it can be retrieved once a job is completed 
def save_job_data(job_data:JobData):
    if not os.path.isdir(JOB_FOLDER):
        os.mkdir(JOB_FOLDER)

    filename = os.path.join(JOB_FOLDER,JOB_TXT)

    mode = "a"
    if not os.path.isfile(filename):
        mode = "w" # Write new file if it does not exist

    with open(filename, mode=mode) as file:
        file.write(job_data.job_id+","+job_data.backend+","+job_data.secret+","+str(job_data.shots)+","+job_data.tag+"\n")

# Load data for all jobs that have been saved and run
def load_job_datas(size:int=None, query_backend:str=None, query_tag:str=None)->list[JobData]:
    job_datas = []
    filename = os.path.join(JOB_FOLDER,JOB_TXT)
    if not os.path.isfile(filename):
        print("No Jobs Found.")
        return job_datas
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            job_id, backend, secret, shots, tag = line.split(',')
            tag = tag.strip()
            data = JobData(job_id, backend, secret, int(shots),tag)

            # Filter based on backend, size and tag
            if (not size == None) and size != len(secret):
                continue
            if (not query_backend == None) and query_backend != backend:
                continue
            if (not query_tag == None) and query_tag != tag:
                continue
            job_datas.append(data)
        
        file.close()
    
    return job_datas