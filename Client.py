import socket
import SecureVault as sv
import datetime
import random
import Helpers
import AESCipher

# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = Helpers.server_address

#IOT device settings
DeviceId = 1337
SessionId = 42

#SecureVault initialization = Key exchange
Vault = sv
Vault.initialize(Helpers.n)

try:
    #Send M1
    M1 = "M1||" + str(DeviceId) +"||"+  str(SessionId)
    client_socket.sendto(M1.encode(), server_address)
    print(Helpers.now() + " M1 send")  
            
    # Receive M2 from server
    data, addr = client_socket.recvfrom(Helpers.buffer_size)
    print(Helpers.now() + " M2 received")
    data = data.decode().split("||")
    tmp = data[0]
    tmp = tmp[1: -1].split(",")
    C1_received = []
    for i in tmp:
        C1_received.append(int(i))

    #C1_received = Helpers.generateChallenge()  #TODO: aus received data rausnehmen

    #Check if r1 has the right value
    r1_received = data[1]

    # Generate key k1 from the keys in the challenge    
    k1 = bytes(Vault.key_length_bits) 
    for i in C1_received:
        k1 = Helpers.xor_bytes(k1, Vault.getKey(i))
        
    t1 = random.randint(0, Helpers.randmax) #random number generated by the IoT device
    C2 = Helpers.generateChallenge()
    
    while set(C2) == set(C1_received):
        C2 = Helpers.generateChallenge()

    r2 = random.randint(0, Helpers.randmax)

    #Send M3 to server
    #TODO: M3 = Enc(k1, r1||t1||{C2,r2})
    M3 = "M3||Enc(" +str(k1) + r1_received + "||" +str(t1)+"||"+"{"+str(C2) + "," + str(r2) + "})"  
    aesInstance = AESCipher.AESCipher(k1)

    nudelholz = str(k1) + r1_received + "||" +str(t1)+"||"+"{"+str(C2) + "," + str(r2) + "}"
    encrypted = aesInstance.encrypt(nudelholz)
    print("Nudelholz: ", nudelholz)
    print("Encrypted: ", encrypted)
    client_socket.sendto(M3.encode(), server_address)
    print(Helpers.now() + " M3 send")  
  
    # Receive M4 from server
    data, addr = client_socket.recvfrom(Helpers.buffer_size)
    message4= data.decode()
    print(Helpers.now() + " M4 received")

    #TODO: decrypt with k2 XOR t1 -> steht r2 drin?

    if(True): #r2 in M4
        print(Helpers.now() + " r2 check succeded")
    else:
        print("r2 check failed ")
except socket.error as e:
        print(f"Something failed: {e}")
finally:
    # Change keys in vault and close the socket
    Vault.changeKeys("irgendwas") #TODO: richtige Message reinschreiben

    client_socket.close()
    print("Client Socket was closed")
