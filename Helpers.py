import random

#Global variables
n = 1000 # size of key vault == number of keys K[0] ... K[n-1]
p = 200  # size of challenge, *p<n* 
randmax = 1e10  
buffer_size = 1024
server_address = ('localhost', 12346) #address of the server


# TODO: description
def generateChallenge():
    challengeSet = []
    while len(challengeSet)<p:
        challengeSet.append(random.randint(0,n-1))
    return challengeSet

# Function to xor two bytes
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))