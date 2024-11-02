# Script contain python code to run the Bernstein Vazirani algorithm on a qauntum computor (or simulator)

from sys import argv

from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator

from rand_bin import rand_bits
from make_qc_oracle import secret_test_qc
from set_service import get_service
from write_results import save_result, ResultData
from save_job import save_job_data, JobData

# Function used to create and run BV quantum circuits based on the inputs specified 
def run_bv(secrets:list[str], run:bool = True, sim:bool = True, shots:int = 4000, backend_name:str = None, save_sim = False, tag:str=""):

    iters = len(secrets) # nuber of unique circuits 
    if run:
        print("Running on Quantum Computer...")

        # Load qiskit credentials
        service = get_service()
        print("Credentials loaded")

        # Find backend
        if backend_name == None:
            n_max = len(max(secrets, key=len))+1 # Highest number of qubits required, used to choose sufficiently large backend 
            backend = service.least_busy(simulator=False, operational=True, min_num_qubits=n_max)
            print("Least busy backend:", backend)
        else:
            backend = service.get_backend(backend_name)
            print("Got backend:", backend)

    for secret in secrets:
        print("Secret: ", secret)

        # Make oracle circuit
        qc = secret_test_qc(secret)

        n = len(secret)
        # Display oracle circuit for single secret if small enough
        if n <= 8 and iters == 1:
            print("Circuit:")
            print(qc.draw())
        
        # Run simulation tests for validation
        if sim and n < 25:
            data = run_local_sim(qc, secret)
            print("Simulation accuracy: " + str(data.accuracy()))
            if save_sim:
                save_result(data)
            assert(data.accuracy() == 1.0)

        # Run on quntum computer
        if run:
            # Transpile qc for backend
            transpiled_qc = transpile(qc, backend)

            # Execute the transpiled circuit 
            job = backend.run(transpiled_qc, shots=shots)
            if tag != None and tag != "":
                job.update_tags(["run_bv_"+secret, tag])
            else:
                job.update_tags(["run_bv_"+secret])

            print("Job ID:", job.job_id())

            # Save job data to be retrieved later
            data = JobData(job.job_id(), backend.name, secret, shots, tag)
            save_job_data(data)
            print("Job data saved")

            # Save circuit traspile data to be used later
            result_data = ResultData(backend.name, secret, shots, counts=None, qc=qc, tqc=transpiled_qc, id=job.job_id())
            save_result(result_data)

    if not run:
        return
          
    if iters > 1:
        print("All jobs queued. Rustles can be loaded once jobs are done.")
    else:
        print("Jobs queued. Rustles can be loaded once job is done.")


# Run a local simulation of quantum circuit
def run_local_sim(qc:QuantumCircuit,secret:str)->ResultData:
    sim_backend = BasicSimulator()
    sim_result = sim_backend.run(qc, shots=shots).result()
    counts = sim_result.get_counts()
    # save result
    data = ResultData(
        sim_backend.name,
        secret,
        shots,
        counts,
        qc
    )
    
    return data

# === Utilities ===

# Generate a series of symbolic quantum register strings where all qubits are the `base_char` except for one target `sweep_char`.
# Return a lists of quantum register strings were each qibit is the target exactly once
# e.g.: 100,010,001
# Originally written by Joshua Jandrell for Quantum lab 1
def sweep_quantum_reg(base_char:chr, sweep_char:chr, numb_bits:int):
    reg_list = []
    for i in range(0,numb_bits):
        reg_list.append((base_char * i) + sweep_char + (base_char * (numb_bits-1-i)))
    return reg_list

# Generate a series of symbolic quantum register strings where all qubits begin as base char but `sweep_char` is filled in from the MSB
# e.g.: 000,100,110,111
def fill_quantum_reg(base_char:chr, sweep_char:chr, numb_bits:int):
    reg_list = []
    for i in range(0,numb_bits+1):
        reg_list.append((sweep_char * i) + (base_char * (numb_bits-i)))
    return reg_list

# === Run from terminal info ===
# prints script usage instructions to the terminal 
def print_instructions():
    print("Usage: ", argv[0]," <options>")
    print(" ")
    print("Options:")
    print("-h \t\t\t\t View Instructions")
    print("-n <number-of-bits> \t\t Specify secret length(s) in comma seperated list [Default = 4]")
    print("-i <number-of-secrets> \t\t Number of random secrets to generate [Default = 1]")
    print("-b <backend-name> \t\t Specify quantum backend")
    print("-s <binary-secrets> \t\t Specify binary secrets to us in a comman seperated list")
    print("-t <string> \t\t\t add a tag to jobs to help load them later")
    print("--sim \t\t\t\t Only run simulation, not quantum computer. Useful for debugging ")
    print("--shots <number-of-shots> \t Number of shots to run [default=4000]")
    print("--sweep \t\t\t Generate all possible secrets where all qubits except one are a 0 for given size")
    print("--fill \t\t\t\t Generate a series of secrets that begins with a secret containing only 0s and slowly fills it with 1s starting from the MSB")

if __name__ == "__main__":

    # Default values
    ns = [4]
    iters = 1
    secrets = None
    shots = 4000
    sim = True
    save_sim = False
    run = True
    backend_name = None
    help_flag = False
    tag = ""

    # Proseduaral options
    sweep = False
    fill = False

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
        elif opt == "-v" or opt == "--version":
            print("Version 1.0")
            help_flag = True
            break
        elif opt == "-n":
            ns = []
            ns = (int(n) for n in argv[i+1].split(','))
            skip_flag = True
        elif opt == "-i":
            iters = int(argv[i+1])
            skip_flag = True
        elif opt == "-s" or opt == "--secrets":
            secrets = argv[i+1].split(',')
            skip_flag = True
        elif opt == "-t" or opt == "--tag":
            tag = argv[i+1]
            skip_flag = True
        elif opt == "-shots" or opt == "--shots":
            shots = int(argv[i+1])
            skip_flag = True
        elif opt == "-sweep" or opt == "--sweep":
            sweep = True
        elif opt == "-fill" or opt == "--fill":
            fill = True
        elif opt == "-sim" or opt == "--sim":
            if sim:
                run = False
                save_sim = True
            else: # Account for case where both -sim and -run were given
                sim = True
        # elif opt == "-run":
        #     if run:
        #         sim = False
        #     else: # Account for case where both -sim and -run were given
        #         run = True
        elif opt == "-b" or opt == "--backend":
            backend_name = argv[i+1]
            skip_flag = True
        else:
            print("Option ", opt, " is not defined.")
            help_flag = True

    if not help_flag:
        if secrets == None:
            secrets = []
            for n in ns:
                if sweep:
                    secrets = secrets + sweep_quantum_reg('0','1',n)
                elif fill:
                    secrets = secrets + fill_quantum_reg('0','1',n)
                else:
                    for i in range(iters):
                        secrets.append(rand_bits(n))
        run_bv(secrets=secrets, run=run, sim=sim, shots=shots, backend_name=backend_name, save_sim=save_sim, tag=tag)