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

def initiate_handshake():
    send_M1()

    try:
        C2 = None
        r2 = None
        while True:
            C2, r2 = receive_message(C2,r2)
            if(C2=="Success"):
                break

    except socket.error as e:
            print(f"Something failed: {e}")
    finally:
        # Change keys in vault and close the socket
        #Vault.changeKeys("irgendwas") #TODO: richtige Message reinschreiben
        client_socket.shutdown(0)
        client_socket.close()
        print("Client Socket was closed")

def receive_message(chal, ran):
    data, addr = client_socket.recvfrom(Helpers.buffer_size)
    print(Helpers.now() + " message received: " + data.decode()[0:2])
    data = data.decode()
    tmp = data.split("||")
    if(tmp[0][0] =="M"):
        data = data.split("||")
    match data[0]:
        case "M2":
            print("M2 arrived")
            C2, r2 = handle_M2(data[1:])
            return C2, r2
        
        case _:
            print("Hopefully M4")
            status = handle_M4(data, chal, ran)
            if(status=="Success"):
                return "Success", "Success"
            #client_socket.shutdown()
            #client_socket.close()
            #print("Client Socket was closed")
    return None, None



def send_M1():
    #Send M1
    M1 = "M1||" + str(DeviceId) +"||"+  str(SessionId)
    client_socket.sendto(M1.encode(), server_address)
    print(Helpers.now() + " M1 send")  


def handle_M2(data):            
    # Receive M2 from server
    tmp = data[0]
    tmp = tmp[1: -1].split(",")
    C1_received = []
    for i in tmp:
        C1_received.append(int(i))

    #Check if r1 has the right value
    r1_received = data[1]

    # Generate key k1 from the keys in the challenge    
    k1 = bytes(Vault.key_length_bits) 
    for i in C1_received:
        k1 = Helpers.xor_bytes(k1, Vault.getKey(i))
        
    t1 = random.randint(0, Helpers.randmax) #random number generated by the IoT device
    C2 = Helpers.generateChallenge()
    
    while set(C2) == set(C1_received): # the challenge has to be different in case of an eavsedropper
        C2 = Helpers.generateChallenge()

    r2 = random.randint(0, Helpers.randmax)

    #Send M3 to server
    #TODO: M3 = Enc(k1, r1||t1||{C2,r2})
    
    print("k1: ", k1)
    print("r1_received: ", r1_received)
    print("t1: ", t1)
    #print("C2: ", C2)
    print("r2: ", r2)

    nudelholz = r1_received + "||" +str(t1)+"||"+"{"+str(C2) + "," + str(r2) + "}" # TODO? Make a set of C2, r2
    encrypted = Helpers.encrypt(k1, nudelholz)
    M3 = "M3||" + str(encrypted) # TODO delete M3|| and fix server if necessary
    print("M3:\n", M3.encode())
    client_socket.sendto(encrypted, server_address)
    print(Helpers.now() + " M3 sent")
    return C2, r2


def handle_M4(message4, C2, r2): 
    # Receive M4 from server
    #data, addr = client_socket.recvfrom(Helpers.buffer_size)
    #message4= data.decode()
    print(Helpers.now() + " M4 received")

    k2 = bytes(Vault.key_length_bits) 
    for i in C2:
        k2 = Helpers.xor_bytes(k2, Vault.getKey(i))

    print("This is m4: ", message4)
    decrypted = Helpers.decrypt(k2, message4)
    #TODO: decrypt with k2 XOR t1 -> steht r2 drin?
    print("Decrypted: \n", decrypted)

    if(decrypted.split("||")[0]==str(r2)): #r2 in M4
        print(Helpers.now() + " r2 check succeded")
        return "Success", "Success"
    else:
        print("r2 check failed ")


initiate_handshake()