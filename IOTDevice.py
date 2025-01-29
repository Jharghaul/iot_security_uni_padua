import logging
import random       # TESTING not for productive use
import socket
import Helpers
import SecureVault as sv
import Database

config = Helpers.load_config()
n = config['globalVariables']['n']

# Configure logging
logging.basicConfig(
    level=config['logging']['level'],  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to the console
)

logger = logging.getLogger(__name__)


# these two have do be defined before the executing code
def read_keys_from_file():
    keys = []
    with open("keys.txt", "rb") as key_file:
        # read keys from file
        for i in range(n):
            keys.append(key_file.readline())
    for i in range(10):
        print(i, len(keys[i]), "\n")
    Vault.setKeys(keys)


def write_keys_to_file(keys):
    with open("keys.txt", "wb") as key_file:
        # Write keys to file
        key_file.writelines(keys)
        for i in range(3):
            print(i, " ", keys[i])


# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (config['server']['host'], config['server']['port'])

# IOT device settings
# TESTING not for productive use, prove of concept, implement here how you get the DeviceID
device_ids = ["123test", "456sensor", "789iot", "112device"]  
DeviceId = random.choice(device_ids)
print(DeviceId)
                      
SessionId = random.randint(1, n) # TESTING implement here how you get the SessionID
buffersize = 1048579

# SecureVault initialization = Key exchange
Vault = sv
keys = read_keys_from_file()
Vault.setKeys(keys)



try:
    # Send M1
    M1 = str(DeviceId) +"||"+  str(SessionId)
    client_socket.sendto(M1.encode(), server_address)
    logger.info("M1 sent")  
            
    # Receive M2 from server
    M2, addr = client_socket.recvfrom(buffersize)
    logger.info("M2 received")
    
    M2 = M2.decode()
    
    # Check if M2 is a error message
    if M2.startswith("error"):
        logger.error("M2 contained error message:")
        raise Exception(M2)
    
    data = M2[1:-1].split("||") # remove { } and split
    tmp = data[0]
    tmp = tmp[1: -1].split(",")
    C1_received = []
    for i in tmp:
        C1_received.append(int(i))
    
    # retrieve r1 for the reply later
    r1_received = data[1]


    
    # Generate encryption key k1 from the keys in the challenge    
    k1 = bytes(Vault.key_length_bits) 
    logger.debug(f"k1 in IOT device: {k1}")
    logger.debug(f"vault(1) in IOT device: : {Vault.getKey(0)}")
    for i in C1_received:
        k1 = Helpers.xor_bytes(k1, Vault.getKey(i))
        
    # Generate random number t1 and challenge C2    
    t1 = Helpers.randInt() 
    C2 = Helpers.generateChallenge()
    
    # Make sure C1 and C2 are not similar to avoid attackers from getting the key
    while set(C2) == set(C1_received):
        C2 = Helpers.generateChallenge()

    r2 = Helpers.randInt()

    # Send M3 to server
    # M3 = Enc(k1, r1||t1||{C2,r2})
    logger.log(Vault.getKey(0))
    message3 = r1_received + "||" + str(t1) + "||" + "{" + str(C2) + "," + str(r2) + "}"
    M3 = Helpers.encrypt(k1, message3)
    client_socket.sendto(M3, server_address)
    logger.info("M3 sent")  
  
    # Receive M4 from server
    data, addr = client_socket.recvfrom(buffersize)
    M4 = data.decode()
    logger.info("M4 received")
    
    # check if M4 is a error message
    if M4.startswith("error"):
        logger.error("M4 contained error message:")
        raise Exception(M4)

    k2 = bytes(Vault.key_length_bits) 
    for i in C2:
        k2 = Helpers.xor_bytes(k2, Vault.getKey(i))

    M4 = Helpers.decrypt(k2, M4)

    message4 = M4.split("||")
    if(message4[0]==str(r2)): #r2 in M4
        logger.debug("r2 check succeded")
    else:
        logger.error("r2 check failed ")

    # compute session key t
    # TESTING use for further communcation
    t = t1^int(message4[1])

    # Change keys in vault and close the socket
    #messages = M1+M2+message3+M4
    #Vault.changeKeys(messages)     # TESTING implement a mechanism to save the new vault keys
    write_keys_to_file(Vault.getKeys)

#except Exception as e:
 #   logger.error(e)
        
finally:
    client_socket.close()
    logger.info("Client Socket was closed")


