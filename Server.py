import socket
import time
import random
import SecureVault as sv


#Define variables
n = 1000 # size of key vault == number of keys K[0] ... K[n-1]
p = 200  # size of challenge, *p<n* 
randmax = 1e10
buffer = 1024

Vault = sv
Vault.initialize(n)

#TODO: eigene Klasse
#Function 
def generateChallenge(amountOfItems):
    challengeSet = []
    while len(challengeSet)<200:
        challengeSet.append(random.randint(0,n-1))
    return challengeSet

def xor_bytes(b1, b2):
    # Ensure both are of the same length
    return bytes(a ^ b for a, b in zip(b1, b2))

#Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12346)
server_socket.bind(server_address)


print("Server is listening on port 12346...")

try:
    #Receive M1 from client
    data, client_address = server_socket.recvfrom(buffer)
    message1 = data.decode()
    print(f"Received data: {message1}")

    #Verify deviceID
    if(True): #TODO: check einbauen
        print("The device is valid")
    else:
        print("Error, aborting, device invalid")
        
    #Generate a random number and the challenge
    r1 = random.randint(0,randmax)
    C1 = generateChallenge(p)

    # Generate key k1 from the keys in the challenge    
    k1 = bytes(512) #TODO: schlüssellänge aus vault
    for i in C1:
        k1 = xor_bytes(k1, Vault.getKey(i))

    #Send M2 back to client
    M2 = str(C1) + str(r1)    #TODO: Tupel
    print("Sent M2")
    server_socket.sendto(M2.encode(), client_address)

    #Receive M3 from client
    data, client_address = server_socket.recvfrom(buffer)
    message3 = data.decode()
    print(f"Received data: {message3}")

    #Verify the IoT devices response

    #TODO: k1?
    #TODO: r1?

    if(False): #TODO: k1 oder r1 passen nicht?
        print("sollte nicht passieren") #TODO: Verbindung mit Client schließen
    else:    
        #Send M4 back to client
        M4 = "2" # TODO Enc(k2^t1, r2||t2)
        server_socket.sendto(M4.encode(), client_address)
        print("Sent M4")
except socket.error as e:
    print(f"Send M4 failed: {e}")

finally:
    # Close the socket
    server_socket.close()
    print("Server Socket was closed")
