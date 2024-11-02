import secrets
from math import ceil
from sys import argv

# Genrates a random n-bit binary stream as a string
def rand_bits(n:int):
    len = ceil(n/8)
    random_byte = secrets.token_bytes(len)
    random_bit = bin(int.from_bytes(random_byte, byteorder='big'))[2:].zfill(8*len)
    return random_bit[0:n]


if __name__ == "__main__":
    random_bit = rand_bits(int(argv[1]))
    print(random_bit)