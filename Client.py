import socket
import SecureVault as sv
import random

#TODO: eigene Klasse
n = 1000 # size of key vault == number of keys K[0] ... K[n-1]
p = 200  # size of challenge, *p<n* 

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
udp_socket.bind(address)

#Device settings
DeviceId = 1337
SessionId = 42
SecureVault = sv
SecureVault.initialize(n)

#Send first message
M1 = str(DeviceId) + str(SessionId)

try:
    udp_socket.sendto(M1.encode(), address)  
except socket.error as e:
    print(f"Send M1 failed: {e}")
        
# Receive M2 from server
data, addr = udp_socket.recvfrom(port)
print(f"Received data: {data.decode()}")

C1_received = generateChallenge(p)  #TODO: aus received data rausnehmen

#Check if correct randomness
if(False):    #TODO: r1 rausziehen r1_received!=r1
    print("Error, not the correct randomness")
    udp_socket.close() 


# Generate key k1 from the keys in the challenge    
k1 = 0 
for i in C1_received:
    k1 = k1^SecureVault.getKey(i) # TODO k1 should be of size m bits now --- test that

t1 = random.randint(0, randmax) #random number generated by the IoT device
C2 = generateChallenge(p)
while(C2.items.sort() == C1_received.items.sort()):
    C2 = generateChallenge(p)
r2 = random.randint(0,randmax)

#Send M3 to server
M3 = "blavlavlavla" #TODO: Enc(k1, r1||t1||{C2,r2})

try:
    udp_socket.sendto(M3.encode(), address)  
except socket.error as e:
    print(f"Send M3 failed: {e}")
    
# Receive M4 from server
data, addr = udp_socket.recvfrom(port)
message4= data.decode()
print(f"Received data: {message4}")

#TODO: decrypt with k2 XOR t1 -> steht r2 drin?

if(True): #r2 in M4
    print("hat alles gepasst. yippieeeehhehhe")
else:
    print("uppsssiiii")

# Change keys in vault and close the socket
SecureVault.changeKeys("irgendwas") #TODO: richtige Message reinschreiben

udp_socket.close()
print("Client Socket was closed")
