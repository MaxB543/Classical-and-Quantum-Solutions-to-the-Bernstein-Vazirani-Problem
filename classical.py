# This script contains classical implementations of the BV and DJ algorithms.

# An oracle that will give a 1-bit output when queried with an n-bit input.
# Output is either constant or calculated using (input dot `a`) mod 2 where `a` is a bainry secret (represented by a string of 1's and 0's)
class Oracle:
    def __init__(self, a:str, constant=False):
        self.__a = a
        self._constant = constant
        self._const_val = a[0] == 1;# Take 1st char of secret string to be constant if constant set
    

    # Perfoems binary operation `a` dot `x` mod 2
    def query(self, x:str):

        if self._constant:
            return self._const_val

        assert(len(self.__a) == len(x))
        res = False # Store final result, initally 0
        for i in range(len(x)):
            if self.__a[i] == '1' and x[i] == '1': 
                res = not res
        return int(res)
    
    def len(self):
        return len(self.__a)
    

# Finds the secret control string, `a,`` for the given oracle. [Oracle should not be constant]
def bv_find(ora:Oracle):
    l = ora.len()
    a = ""
    for i in range(l):
        # Construt x strign to query from oracle
        x = ('0' * i) + '1' + ('0' * (l-1-i))

        # query oracle and construct string accordingly
        if ora.query(x):
            # Output is a 1 so the secret must have a 1 in this position.
            a += "1"
        else:
            a += "0"

    return a, l

# Checks to see if the oracle is balanced or constant, returns true if constant 
# Also returns number of cycles taken to find if constant or not
def dj_find_constant(ora:Oracle):
    l = ora.len()
    half_vals = int(((2**l)/2)) + 1 # Must check at least half all posibe values plus 1 more to detemrine if function is constant
    ref = ora.query('0' * l)
    for i in range(1, half_vals):
        # Construct query string 
        x = bin(i)[2:].zfill(l)
        if ora.query(x) != ref:
            return False, i+1
    
    # No alternate value has been found, function cannot be balanced so must be constant
    return True, half_vals