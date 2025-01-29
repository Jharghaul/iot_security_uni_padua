import base64
import hashlib
from Crypto import Random # pip install --upgrade pycryptodome 
from Crypto.Cipher import AES
import SecureVault as sv
import urllib.parse as url

Vault = sv.SecureVault()
n = 1000

Vault.initialize()
print("Test")
print(len(Vault.getKeys()))



def write_keys_to_file(keys):
    with open("keys_original.txt", "wb") as key_file:
   
        # Write keys to file
        for i in range(n):
            #encodedKey = Vault.getKey(i).decode('utf-8')
            key_file.write(Vault.getKey(i))
            #key_file.write("\n")
            if i <= 3:
                print(i, keys[i])
                #print("type: ", type(keys[i]))

def write_keys_to_files_ugly(keys):
    filepath = "key_"
    for i in range(n):
        print("ups")
        

write_keys_to_file(Vault.getKeys())
print()
#read_keys_from_file()


# python C:\Users\grane\Documents\GitHub\iot_security_uni_padua\

#print("AES.block_size", str(AES.block_size))

# b'\x18_\x8d\xb3"q\xfe%\xf5a\xa6\xfc\x93\x8b.&C\x06\xec0N\xdaQ\x80\x07\xd1vH&8\x19i'
# b"\x19\\j\\\xcc~\x82\x8b\x0f\r\x186'1\xc6\x1c|B\xb2:M\x10\xbd\xc7r\xa4=i\xeb\xb0\xa0\x9bu\x98\xea\xa0\x83\x93Z\x00o3\xe3\nA\x06%\x8cN~\xb0\xd0\xd7co \x05\x90\xb5\x02G\xc2\xd5\xbc"