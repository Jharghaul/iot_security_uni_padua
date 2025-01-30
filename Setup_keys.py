from Crypto import Random # pip install --upgrade pycryptodome 
from Crypto.Cipher import AES
import SecureVault as sv
import urllib.parse as url
import Helpers

config = Helpers.load_config()
vault = sv.SecureVault()
n = config['globalVariables']['n'] # amount of Keys
vault.initialize()

def write_keys_to_file(vault):
    with open("keys_original.txt", "wb") as key_file:
   
        # Write keys to file
        for i in range(n):
            key_file.write(vault.getKey(i))

      
write_keys_to_file(vault)