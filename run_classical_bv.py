# Script used to run the classical solution to the BV problem for demonstrative purposes 

from sys import argv

from classical import Oracle, bv_find
from rand_bin import rand_bits

def classical_bv_demo(secret:str):
    # Make oracle
    ora = Oracle(secret)
    n = ora.len()

    print(f"{n}-bit oracle created (unknown secret={secret}).")

    _secret = "_"*n
    print(f"Secret: {_secret}")
    for i in range(n):
        print("=================================================")
        # Construt x strign to query from oracle
        x = ('0' * i) + '1' + ('0' * (n-1-i))
        y = ora.query(x)
        print(f"Query {i}: \n\tInput: {x} \n\toutput: {y}")
        print()
        print(f"Based on the output, bit {i} must be a {y}")
        print()
        _secret = _secret[0:n-1-i] + str(y) + _secret[n-i:]
        print(f"Secret: {_secret}")
        print()
    print("=================================================")
    print(f"Found secret: {_secret} (Oracle secret is {secret})")


if __name__ == "__main__":
    if len(argv) == 1:
        a = rand_bits(4)
    else:
        a = argv[1]

    classical_bv_demo(a)