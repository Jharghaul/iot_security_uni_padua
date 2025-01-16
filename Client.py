import logging
import socket
import Helpers
import SecureVault as sv


config = Helpers.load_config()

# Configure logging
logging.basicConfig(
    level=config['logging']['level'],  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to the console
)

logger = logging.getLogger(__name__)

# Client socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (config['server']['host'], config['server']['port'])

#IOT device settings
DeviceId = 1337
SessionId = 42

#SecureVault initialization = Key exchange
Vault = sv
Vault.initialize()

try:
    #Send M1
    M1 = str(DeviceId) +"||"+  str(SessionId)
    client_socket.sendto(M1.encode(), server_address)
    logger.info(" M1 sent")  
            
    # Receive M2 from server
    data, addr = client_socket.recvfrom(config['globalVariables']['buffersize'])
    logger.info(" M2 received")
    
    data = data.decode()[1:-1].split("||") # remove { } and split
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
        
    # Generate random number t1 and challenge C2    
    t1 = Helpers.randInt() 
    C2 = Helpers.generateChallenge()
    
    while set(C2) == set(C1_received):
        C2 = Helpers.generateChallenge()

    r2 = Helpers.randInt()

    #Send M3 to server
    #TODO: M3 = Enc(k1, r1||t1||{C2,r2})
    message3 = r1_received + "||" +str(t1)+"||"+"{"+str(C2) + "," + str(r2) + "}" # TODO? Make a set of C2, r2
    M3 = Helpers.encrypt(k1, message3)
    client_socket.sendto(M3, server_address)
    logger.info("M3 sent")  
  
    # Receive M4 from server
    data, addr = client_socket.recvfrom(config['globalVariables']['buffersize'])
    message4= data.decode()
    logger.info("M4 received")

    k2 = bytes(Vault.key_length_bits) 
    for i in C2:
        k2 = Helpers.xor_bytes(k2, Vault.getKey(i))

    logger.debug(f"This is M4: {message4}")
    decrypted = Helpers.decrypt(k2, message4)
    #TODO: decrypt with k2 XOR t1 -> steht r2 drin?
    logger.debug(f"Decrypted: {decrypted}")

    if(decrypted.split("||")[0]==str(r2)): #r2 in M4
        logger.debug("r2 check succeded")
    else:
        logger.error("r2 check failed ")
        #TODO: error werfen


except socket.error as e:   # TODO: feineres Error Handling
        logger.error(f"Something failed: {e}")
        
finally:
    # Change keys in vault and close the socket
    Vault.changeKeys("irgendwas") #TODO: richtige Message reinschreiben

    client_socket.close()
    logger.info("Client Socket was closed")
