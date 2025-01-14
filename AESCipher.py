

import base64
import hashlib
from Crypto import Random # pip install --upgrade pycryptodome 
from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        
        if(type(key)==type("Hello")):
            self.key = hashlib.sha256(key.encode()).digest()
        else:
            self.key = key
        print("AESCIpherkey: ", self.key)
        
        print("key(hello) len: ", len(hashlib.sha256("Hello".encode()).digest()), "\n", hashlib.sha256("Hello".encode()).digest())
        print(key)
        print("len(key): ", len(key))
        #self.key = hashlib.sha256("Hello".encode()).digest() # FIXME delete line
        

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]