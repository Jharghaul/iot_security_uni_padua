import socket
import time
import random

#Define variables
n = 1000 # size of key vault == number of keys K[0] ... K[n-1]
p = 200  # size of challenge, *p<n* 
randmax = 1e10

#TODO: eigene Klasse
#Function 
def generateChallenge(amountOfItems):
    challengeSet = {}
    while len(challengeSet<200):
        challengeSet.add(random.randint(0,n-1))
    return challengeSet


#Create socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Destination address and port
address = ('localhost', 12345)
port = 1024

#Receive M1 from client
data, addr = udp_socket.recvfrom(port)
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
k1 = 0 
for i in C1_received:
    k1 = k1^SecureVault.getKey(i) # TODO k1 should be of size m bits now --- test that

#Send M2 back to client
try:
    M2 = str(C1) + str(r1)    #TODO: Tupel
    udp_socket.sendto(message.encode(M2), address)
except socket.error as e:
    print(f"Send M2 failed: {e}")
    
#Receive M3 from client
data, addr = udp_socket.recvfrom(port)
message3 = data.decode()
print(f"Received data: {message3}")

#Verify the IoT devices response

#TODO: k1?
#TODO: r1?

if(False): #TODO: k1 oder r1 passen nicht?
    print("sollte nicht passieren") #TODO: Verbindung mit Client schließen
    
#Send M4 back to client
try:
    M4 = 2 # TODO Enc(k2^t1, r2||t2)
    udp_socket.sendto(message.encode(M4), address)
except socket.error as e:
    print(f"Send M4 failed: {e}")

# Close the socket
udp_socket.close()
print("Server Socket was closed")
