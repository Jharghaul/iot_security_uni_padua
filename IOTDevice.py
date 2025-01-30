import logging
import random       # TESTING not for productive use
import socket
import Helpers
import SecureVault as sv
import base64

config = Helpers.load_config()
n = config['globalVariables']['n']

# Configure logging
logging.basicConfig(
    level=config['logging']['level'],  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to the console
)
logger = logging.getLogger(__name__)

# Reads all keys from a binary file
def read_keys_from_file(device_ID):
    keys = []
    file = device_ID+"_keys.txt"

    with open(file, "rb") as key_file:
        # Read keys from file
        all_keys = key_file.read()
        logger.debug(f"blob length: {len(all_keys)}")

        # separate keys 
        for i in range(n):
            single_key = all_keys[i*32:(i+1)*32]
            keys.append(single_key)
            
    return keys

# Writes all keys to a binary file
def write_keys_to_file(keys, device_ID):
    file = device_ID+"_keys.txt"
    with open(file, "wb") as key_file:
   
        # Write keys to file
        for i in range(n):
            key_file.write(vault.getKey(i))
           
# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (config['server']['host'], config['server']['port'])

# IOT device settings
# TESTING not for productive use, prove of concept, implement here how you get the DeviceID
deviceIDs = ["123test", "456sensor", "789iot", "112device"]  
deviceID = random.choice(deviceIDs)
logger.debug(f"{deviceID}")
                      
sessionID = random.randint(1, n) # TESTING implement here how you get the SessionID
buffersize = 1048579

# SecureVault initialization from file
vault = sv.SecureVault()
keys = read_keys_from_file(deviceID)
vault.setKeys(keys)

try:
    # Send M1
    M1 = str(deviceID) +"||"+  str(sessionID)
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
    
    data = M2[1:-1].split("||") # Remove { } and split
    tmp = data[0]
    tmp = tmp[1: -1].split(",")
    C1_received = []
    for i in tmp:
        C1_received.append(int(i))
    
    # Retrieve r1 for the reply later
    r1_received = data[1]


    # Generate encryption key k1 from the keys in the challenge    
    k1 = bytes(vault.key_length_bits) 
    logger.debug(f"k1 in IOT device: {k1}")
    logger.debug(f"vault(1) in IOT device: : {vault.getKey(0)}")
    for i in C1_received:
        k1 = Helpers.xor_bytes(k1, vault.getKey(i))
        
    # Generate random number t1 and challenge C2    
    t1 = Helpers.randInt() 
    C2 = Helpers.generateChallenge()
    
    # Make sure C1 and C2 are not similar to avoid attackers from getting the key
    while set(C2) == set(C1_received):
        C2 = Helpers.generateChallenge()

    r2 = Helpers.randInt()

    # Send M3 to server
    # M3 = Enc(k1, r1||t1||{C2,r2})
    logger.debug(f"Vault key 0 before sending M3: {vault.getKey(0)}")
    message3 = r1_received + "||" + str(t1) + "||" + "{" + str(C2) + "," + str(r2) + "}"
    M3 = Helpers.encrypt(k1, message3)
    client_socket.sendto(M3, server_address)
    logger.info("M3 sent")  
  
    # Receive M4 from server
    data, addr = client_socket.recvfrom(buffersize)
    M4 = data.decode()
    logger.info("M4 received")
    
    # Check if M4 is a error message
    if M4.startswith("error"):
        logger.error("M4 contained error message:")
        raise Exception(M4)

    k2 = bytes(vault.key_length_bits) 
    for i in C2:
        k2 = Helpers.xor_bytes(k2, vault.getKey(i))
    
    k2 = Helpers.xor_bytes(k2, t1.to_bytes(64, "little"))
    
    M4 = Helpers.decrypt(k2, M4)

    message4 = M4.split("||")
    if(message4[0]==str(r2)): #r2 in M4
        logger.debug("r2 check succeded")
    else:
        logger.error("r2 check failed ")
        raise ValueError("r2 was not correct")

    # Compute session key t
    # TESTING use for further communcation
    t2 = message4[1]
    t = t1^int(t2)

    # Change keys in vault and in file for storage
    messages = M1+M2+message3+M4
    vault.changeKeys(messages)
    write_keys_to_file(vault.getKeys(), deviceID)

except Exception as e:
    logger.error(e)
        
finally:
    # Close the socket
    client_socket.close()
    logger.info("Client Socket was closed")


