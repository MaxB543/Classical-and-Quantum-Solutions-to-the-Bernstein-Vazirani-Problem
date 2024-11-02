# Script used to load and display results from runs on quantum computers
from sys import argv

from set_service import get_service
from save_job import load_job_datas
from write_results import save_result, write_to_csv, ResultData

# Retrieves jobs from qiskit and writes data for all results
def save_loaded_results(n:int = None, backend:str = None, tag:str = None):

    # Load job datas from local file
    job_datas = load_job_datas(n,backend,tag)

    if len(job_datas) == 0:
        print("No jobs found.")
        return

    # Load credentials
    service = get_service()
    print("Credentials loaded.")
    
    for job_data in job_datas:

        # Load job from IBM qiksit
        job = service.job(job_data.job_id)

        if job.done():
            # Save result data
            counts = job.result().get_counts()
            result_data = ResultData(job_data.backend, job_data.secret, job_data.shots, counts, tag=job_data.tag)

            # Print output for user feedback
            print(result_data.backend + "(" + result_data.secret + ") created: " + str(job.creation_date) + " ran with accuracy " + str(result_data.accuracy()))
            save_result(result_data)
            print("Saved results.\n")
        else:
            print(job_data.backend + "(" + job_data.secret + ") created: " + str(job.creation_date) + " is not done.")

def print_instructions():
    print("Usage: ", argv[0]," <options>")
    print(" ")
    print("Options:")
    print("-h \t\t\t View Instructions")
    print("-n <int> \t\tNumber of bits\t\t[Default = any]")
    print("-b <backend_name> \tSpecify quantum backend\t[Default = any]")
    print("-t <tag> \tSpecify a tag that the jobs should have\t[Default = any]")

if __name__ == "__main__":
    n = None
    backend = None
    help_flag = False
    tags = None
    # Process arguments
    skip_flag = False
    for i in range(1, len(argv)):
        if skip_flag:
            skip_flag =False
            continue
        opt = argv[i]
        if opt == "-h" or opt == "--help":
            print_instructions()
            help_flag = True
            break
        if opt == "-v" or opt == "--version":
            print("Version 1.0")
            help_flag = True
            break
        elif opt == "-n":
            n = int(argv[i+1])
            skip_flag = True
        elif opt == "-b" or opt == "--backend":
            backend = argv[i+1]
            skip_flag = True
        elif opt == "-t" or opt == "--tag":
            tags = argv[i+1].strip().split(',')
            skip_flag = True
        else:
            print("Option ", opt, " is not defined.")
    if not help_flag:
        if tags == None:
            save_loaded_results(n=n,backend=backend)
        else:
            for tag in tags:
                save_loaded_results(n=n,backend=backend,tag=tag)

