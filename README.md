# ELEN4022 PROJECT: Classical and Quantum Solutions to the Bernstein Vazirani Problem 

This repository contains python scripts used to implement and investigate classical and quantum solutions to the Bernstein-Vazirani problem which has applications in cyber security and cryptanalysis.

The problem involves querying an n-bit oracle with function, $f(x)\in\\{0,1\\}$, to determine the n-bit binary secret, $s$, which controls the oracle output. $f(x)$ is promised to be the binary dot product of input $x$ and secret $s$ under modulo 2. 

$f(x) = (x\bullet s)\mod 2$

The most time-efficient ($O(n)$ time-complexity) classical algorithm is implemented along with the Bernstein-Vazirani quantum algorithm which uses a restricted case of the Deutsch-Jozsa algorithm to determine the secret with $O(1)$ time complexity.

Although the quantum algorithm is theoretically deterministic, it is prone to random noise-related errors the current era of noisy intermediate quantum computing. The python scripts in this repository are used to automate the execution of the Bernstein-Vazirani algorithm on IBM’s fleet of quantum computers and quantify the practical susses rate. The scrips allow for varied secret length and structure so that the effects of secret bit count, density of 1s and position of 1s may be investigated. Results are recorded in `.csv` with circuit layouts in `.tex` files for further analysis.

## Run the classical approach 
The most effective classical approach to solving the Bernstein-Vazirani problem leverages the nature of the inner dot product. If a query register, $x$ has a value of `0` for all but one bit ($x_n$ = `1`) then the oracle output will depend only on $x_n \bullet s_n$. The oracle will return `1` if and only if the secret has a value of `1` in the same position as the `1` in the query register. The secrete can be found in $O(n)$ time by repeating this process for each of its bits.

The `run_classical_bv.py` script can be run to demonstrate this algorithm.
```bash 
python run_classical_bv.py <secret>
```
The script will output each query call and the secret with unknow bit represented by '_'.

## Setup
All scripts should be run inside a python virtual environment (`venv`) with all necessary dependences installed. Use the `make_venv.bs` script  to create such an environment and install decencies using `pip`.
```bash
bash make_venv.bs
```
The `venv` will be created in the `.venv/` directory. The following commands can be used to activate this environment:
### For Linux and MacOs:
```bash
source .venv/bin/activate
```
### For Windows:
```bash
source .venv/Scripts/activate
```
Once the `venv` is activated all scripts can be run.
### Dependencies 
If dependency management system is preferred or for some reason the above method does not work, the following packages must be installed to run python scripts and jupyter notebooks.

- `qiskit` to create and simulate quantum circuits. 
- `qiskit-ibm-runtime` to run quantum circuits on real IBM quantum computers.
- `matplotlib` to plot circuit diagrams and histograms.
- `pylatexenc` to plot large circuit diagrams.

## Run Bernstein-Vazirani on a Quntum Computer

The `run_bv.py` script can be used to run the Bernstein-Vazirani algorithm on a quantum computer. This script provides a convent way to construct and test batches of quantum oracles on IBM quantum computers. 
Job queue times can be long on IBM compute resources. To avoid delays in execution this script does not wait for jobs to be completed. Job is saved and results may be retired using the `load_results.py` script after the job is complete. 

To execute `run_bv.py` use the following format:
```bash
python run_bv.py <option-list>
```
|⚠️|The system will prompt the user for an and IBM quantum API token when it is run for the first time.|
|:--:|:--:|

`<option-list>` is a list of options specifying how oracles will be constructed and where the test circuits should be run. The script will display a full list of available options when run with the `-h` or `--help` option. 

If no options are specified, the default behaviour is to run a single random 4-qubit secret on the least busy IBM quantum backend 

Some notable options included:

|Option | Description| Example | Explanation|
|:--:|:--:|:--:|:--:|
|`-n <numb-bits>`| Specify the secret length| `python run_bv.py -n 3,6`|Run a 3-bit secrete and 6-bit secrete|
|`-i <numb-secrets>`|Specify the number of secretes |`python run_bv.py -n 4 -i 8`|Run 8 different 4-bit secrets|
|`-s <secrets>`|Specify secrets to be used|`python run_bv.py -s 10,010,0010`|Run secrets `10`, `010` and `0010`
|`-b <backend>`|Specify the backend| `python run_bv.py -s 101 -b ibm_hanoi`|Run on ibm_hanoi|
|`-t <tag>`| Specify tag of retrieval |`python run_bv.py -i 8 -t random`| Tag all results as 'random' |

|ℹ️| Tags can be used to retrieve test resuls with `load_results.py` or to find jobs in the IBM quantum job list.|
|:--:|:--:|

|ℹ️| For IBM only, all test circuit jobs are automatically tagged baed on their secret with format `run_bv_<secret>`|
|:--:|:--:|

### Circuit Validation 
The validation process is implemented as fail-safe to avoid wasting public IBM compute resources on incorrectly constructed circuits in the unlikely event that code updates cause the circuit construction system to fail.
|ℹ️| Over 800 quantum circuits have been validated.  Failures are not expected.|
|:--:|:--:|

Each oracle circuit constructed by `run_bv.py` is simulated using the  Qiskit `BasicBackend` to verify that the circuited constructed is theoretically valid in ideal conditions. The simulation accuracy (printed to the consol) should always be 1.0. If the Bernstein-Vazirani simulation does not identify the oracle with 1.0 accuracy the script is terminated.

### Jobs directory
Tags and ids for all jobs created using the `run_bv.py` system are saved in the `.qiksit_jobs/` directory so that they may be retrieved from IBM Quantum at any point.

|❗|Do not delete the `.qiksit_jobs/` directory or modify its contents.|
|:--:|:--:|

## Load results

After Jobs have been complete results may be loaded using the `load_results.py` script. This script will save output counts and accuracy information in a `.csv` file for further analysis. Histograms of output counts are also plotted. 

The script has the following usage:
```bash
python load_results.py <option-list>
```

The `<option-list>` can be used to specify that only results with the given secret length, backend name, or tag are loaded. For a list of all options run `load_results.py` with the `-h` option or see the table below.
When `<option-list>` is left blank all results are loaded by default. 

|Option | Description|
|:--:|:--:|
|`-n <numb-bits>`| Specify secret length, only one allowed| 
|`-b <backend>`|Specify backend name, only one allowed|
|`-t <tag>`| Specify tag(s), more that one as comma seperated list |

Restriction can be combined, for example: `python load_results.py -n 3 -t count,test -b ibm_nazca` will only load results for 3-qubit oracles tagged 'count' or 'test' from ibm_nazca.

### The accuracy measure
When results are loaded the 'accuracy' of a particular run is calculated and displayed. This value is the success rate of the Bernstein-Vazirani algorithm found by dividing the number of shots where the quantum circuit output the correct secret by the total number of shots run.

### Tables
Two `.csv` files are updated whenever `load_results.py` is run. These files contain test and accuracy information to be used for further analysis.
1.	`results/results_accuracy.csv` contains backend name, secret value, secret length ('size'), and tag information.
2.	`results/results_<secret_length>.csv` contains backend, secret and output information as well as the frequnecy of each classical circuit output register.

   
|⚠️|If these files already exist, results will be appended to them.|
|:--:|:--:|

### Additional information
Additional information, including histograms and `.tex` files to plot quantum circuits can be found in the directory `results/secrets/secret_<secret>/` Files are named based on backend and job id.

## Test Results 
Select results from over 700 tests (used to retrieve the data presented in the final report) can be found in the `ref_results/` folder.

## Plot Test Results in MATLAB
To plot the results, upload all 5 MATLAB scripts from the `MATLAB plots` folder into a MATLAB IDE. Within the same directory that contains the scripts, copy in the **most recent** "results_accuracy.csv".

Generate each of the graphs by running the three scripts ending in __exp_ .




