import base64
import hashlib
from Crypto import Random # pip install --upgrade pycryptodome 
from Crypto.Cipher import AES

C1 = [666, 985, 976, 299, 879, 429]
C2 = [588, 666, 985, 976, 299, 879, 429, 247, 825, 99, 668, 561, 80, 569, 762, 824, 218, 56, 160, 581, 522, 905, 400, 958, 72, 299, 344, 237, 291, 387, 851, 989, 501, 234, 747, 733, 794, 966, 4, 890, 635, 148, 893, 800, 535, 297, 731, 108, 793, 269, 103, 453, 84, 404, 382, 774, 614, 687, 217, 573, 657, 796, 48, 50, 865, 416, 142, 385, 932, 608, 861, 186, 548, 303, 842, 16, 21, 168, 68, 737, 765, 329, 879, 873, 863, 523, 985, 581, 220, 106, 811, 968, 109, 494, 960, 66, 398, 512, 367, 355, 391, 907, 25, 129, 87, 975, 492, 826, 949, 665, 725, 956, 58, 546, 299, 711, 557, 483, 30, 484, 267, 215, 527, 245, 882, 469, 813, 498, 475, 75, 290, 970, 317, 725, 418, 140, 569, 684, 380, 92, 137, 273, 777, 466, 957, 390, 931, 422, 586, 645, 371, 20, 310, 313, 447, 126, 409, 181, 991, 786, 426, 8, 847, 82, 71, 991, 895, 121, 699, 716, 149, 480, 842, 686, 736, 475, 686, 672, 966, 585, 471, 305, 17, 810, 465, 135, 118, 679, 407, 499, 112, 906, 95, 951, 693, 638, 476, 355, 122, 594]
ph = "r1||t1||{[588, 666, 985, 976, 299, 879],r2}"
ph = ph.split("||")
print(ph)
ph = ph[2][1:-1]
print(ph)
ph = ph[1:(ph.find(ph.split(",")[-1])-2)]
print(ph)

import SecureVault as sv
vault = sv

vault.initialize()

keys = vault.getKeys()

with open("keys.txt", "wb") as key_file:
    for i in range(len(keys)):
        key_file.write(vault.getKey(i))
        if(vault.getKey(i) != keys[i]):
            print("Interesting")


# python C:\Users\grane\Documents\GitHub\iot_security_uni_padua\

#print("AES.block_size", str(AES.block_size))

# b'\x18_\x8d\xb3"q\xfe%\xf5a\xa6\xfc\x93\x8b.&C\x06\xec0N\xdaQ\x80\x07\xd1vH&8\x19i'
# b"\x19\\j\\\xcc~\x82\x8b\x0f\r\x186'1\xc6\x1c|B\xb2:M\x10\xbd\xc7r\xa4=i\xeb\xb0\xa0\x9bu\x98\xea\xa0\x83\x93Z\x00o3\xe3\nA\x06%\x8cN~\xb0\xd0\xd7co \x05\x90\xb5\x02G\xc2\xd5\xbc"