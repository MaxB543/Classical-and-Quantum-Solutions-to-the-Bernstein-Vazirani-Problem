# Contains code to create a qiskit quantum circuit object for and oracle to be used in bv (or dj) testing
# Code was written with reference to the IBM repo: https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/algorithms/bernstein_vazirani.ipynb

from qiskit import QuantumCircuit

# Adds appropriate gates to construct a quantum oracle controlled by the given secrete to qc
# It is assumed that qc has the correct number of qubits and classical bit
# secret number should be in big endian notation
def add_secret_oracle(qc:QuantumCircuit, secret: str):
    # iterate through secret from LSB to MSB
    for i, bin_digit in enumerate(reversed(secret)):
        if bin_digit == '1':
            qc.cx(i,len(secret)) # The bit after the secret number will be the oracle output

    return qc

# Creates a qiskit quantum circuit used to test a quantum oracle with the following secret
# secret should be given as a binary string in bin endian format 
def secret_test_qc(secret:str):

    # The number of inputs to oracle 
    n = len(secret)
    # Create appropratle sized quatum circuit
    qc = QuantumCircuit(n+1,n)
    # Place H-gates on all oracle inputs
    qc.h(range(n))
    # Add and X-gate and H-gate to oracle output qibit
    qc.x(n)
    qc.h(n)

    qc.barrier()

    # Place oracle on secret
    qc = add_secret_oracle(qc, secret)

    qc.barrier()

    # place H-gates on output
    qc.h(range(n))

    qc.barrier()

    # Measure quantum and classical register
    qc.measure(range(n),range(n))

    return qc