import socket
import time

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

#Receive data from client
data, addr = udp_socket.recvfrom(port)
print(f"Received data: {data.decode()}")

#Verify deviceID
if(true): #TODO: check einbauen
    print("The device is valid")
else:
    print("Error, aborting, device invalid")
    
#Generate a random number and the challenge
r1 = random.randint(0,randmax)
C1 = generateChallenge(p)

#Send second message back to client
try:
    M2 = str(C1) + str(r1)    #TODO: Tupel
    udp_socket.sendto(message.encode(M2), address)
except socket.error as e:
    print(f"Send M2 failed: {e}")
        


# Close the socket
udp_socket.close()