import random
import datetime
import AESCipher
import SecureVault

#Global variables
n = SecureVault.getN() # size of key vault == number of keys K[0] ... K[n-1]
p = SecureVault.getP()  # size of challenge, *p<n*
randmax = int(1e10)
buffer_size = 1024*1024
server_address = ('localhost', 12346) #address of the server


# generate a challange
def generateChallenge():
    challengeSet = []
    while len(challengeSet)<p:
        challengeSet.append(random.randint(0,n-1))
    return challengeSet

# xors two bytes b1 and b2
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# returns the current time as a string
def now():
    return str(datetime.datetime.now().time())

# AES encrypts a message under the given key
def encrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.encrypt(message)

# AES encrypts a message under the given key
def decrypt(key, message):
    aesInstance = AESCipher.AESCipher(key)
    return aesInstance.decrypt(message)


