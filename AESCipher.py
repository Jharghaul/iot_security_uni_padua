import base64
from Crypto import Random # pip install --upgrade pycryptodome 
from Crypto.Cipher import AES


class AESCipher(object):
    
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key
        
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cipher_decrypted = cipher.decrypt(enc[AES.block_size:])
        return AESCipher._unpad(cipher_decrypted).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]