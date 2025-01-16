import random
import datetime
import AESCipher
import json

#Global variables
#n = 1000    # size of key vault == number of keys K[0] ... K[n-1]   #TODO
#p = 200     # size of challenge, *p<n*                              #TODO
#randmax = int(1e10)
#buffer_size = 1024*1024
#server_address = ('localhost', 12346) #address of the server

# get data from config.json
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# generate a challange
def generateChallenge():
    config = load_config()
    n = config['globalVariables']['n']
    p = config['globalVariables']['p']
    
    challengeSet = []
    while len(challengeSet)<p:
        challengeSet.append(random.randint(0,n-1))
    return challengeSet

# xors two bytes b1 and b2
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# AES encrypts a message under the given key
def encrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.encrypt(message)

# AES encrypts a message under the given key
def decrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.decrypt(message)


