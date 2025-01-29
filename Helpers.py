import random
import AESCipher
import json
import pathlib

# Get data from config.json
def load_config():
    current_directory = pathlib.Path(__file__).parent.resolve()
    with open(str(current_directory) + '/config.json', 'r') as f:
        config = json.load(f)
    return config

# Generate a challenge
def generateChallenge():
    config = load_config()
    n = config['globalVariables']['n']
    p = config['globalVariables']['p']
    
    challengeSet = set()
    while len(challengeSet)<p:
        index = random.randint(0,n-1)
        
        # Make sure that distinct values are chosen
        while index in challengeSet:
            index = random.randint(0,n-1)
            
        challengeSet.add(index)
    return challengeSet

# xors two bytes b1 and b2
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# AES encrypts a message under the given key
def encrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.encrypt(message)

# AES decrypts a message under the given key
def decrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.decrypt(message)

# Generate random int between 0 and randmax
def randInt():
    config = load_config()
    return random.randint(0, config['globalVariables']['randmax'])