import random
print("hello world")

n = 1000 # size of key vault == number of keys K[0] ... K[n-1]
p = 200  # size of challenge, *p<n* 
randmax = 1e10

def generateChallenge(amountOfItems):
    challengeSet = {}
    while len(challengeSet<200):
        challengeSet.add(random.randint(0,n-1))
    return challengeSet


# IoT Device
DeviceId = 1337
SessionId = 42
SecureVault = [] # placeholder for secure vault
for i in range(1000): 
    SecureVault.append(i)

M1 = str(DeviceId) + str(SessionId)
#TODO send M1 to server


# TODO Receive M2={C1,r1}
C1_received = {0,1,2,3}
# if(r1_received!=r1):
#   print("Error, not the correct randomness")
#   return

# Generate key k1 from the keys in the challenge
k1 = 0 
for i in C1_received:
    k1 = k1^SecureVault[i] # TODO Test if this is correct
# TODO k1 should be of size m bits now --- test that

t1 = random.randint(0, randmax) #random number generated by the IoT device
C2 = generateChallenge(p)
while(C2.items.sort() == C1_received.items.sort()):
    C2 = generateChallenge(p)
r2 = random.randint(0,randmax)
# M3 = Enc(k1, r1||t1||{C2,r2})
# TODO send M3



########### Server ###############

# verfiy the device is valid
# TODO receive message
if(DeviceId==1337):
    print("The device is valid")
else:
    print("Error, aborting, device invalid")
#generate a random number r1
r1 = random.randint(0,randmax)

#generate a challenge C1

C1 = generateChallenge(p)
# TODO send message M2={C1,r1}

# TODO receive M3
# TODO verify the IoT devices response

M4 = 2 # TODO Enc(k2^t1, r2||t2)
# TODO send M4

