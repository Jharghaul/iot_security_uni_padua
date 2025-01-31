import logging
import socket
import Database
import Helpers
import SecureVault as sv

vault = sv.SecureVault()
vault.initialize()

config = Helpers.load_config()

# Configure logging
logging.basicConfig(
    level=config['logging']['level'],
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Log to the console
)
logger = logging.getLogger(__name__)

def start_server():
    # Server setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (config['server']['host'], config['server']['port'])
    server_socket.bind(server_address)

    logger.info(f"Server is listening on port {config['server']['port']} ...")

    # Database initialization
    Database.create_database()

    try:
        while True:
            handle_client(server_socket)

    except Exception as e:   
       logger.error(f"Exchange failed: {e}")

    finally:
        # Close the socket
        server_socket.close()
        logger.info("Server Socket was closed")
        
        
def handle_client(server_socket):
    
    try:
        # Receive M1 from client
        data, client_address = server_socket.recvfrom(config['globalVariables']['buffersize'])
        M1 = data.decode()
        logger.info(f"{client_address}: Received M1")
        logger.debug(f"M1: {M1}")
        message1 = M1.split("||")
        deviceID = message1[0]

        # Verify deviceID
        if(Database.is_valid_device_id(deviceID)):
            logger.info(f"{client_address}: The device is valid")
            keys = Database.get_vault_of(deviceID)
            logger.debug(f"{client_address}: keys are set")
            vault.setKeys(keys)
            logger.debug(f"{client_address}: vault is set")
            
        else:
            logger.error(f"{client_address}: Error, aborting, device invalid")
            raise ValueError("Invalid device ID")
            
        # Generate a random number r1 and the challenge C1
        r1 = Helpers.randInt()
        C1 = Helpers.generateChallenge()
        logger.debug(f"{client_address}: C1 generated")
        
        # Generate encryption key k1 from the keys in the challenge C1
        # IoTDevice does the same on it's side 
        k1 = bytes(vault.key_length_bits)
        for i in C1:
            k1 = Helpers.xor_bytes(k1, vault.getKey(i))
            
        logger.debug(f"{client_address}: k1 generated: {k1}")

        # Send M2 back to IoT device
        # M2 = { C1 || r1 }
        M2 = "{" + str(C1) + "||" + str(r1) + "}"
        logger.debug(f"M2: {M2}")
        logger.info(f"{client_address}: Sent M2")
        server_socket.sendto(M2.encode(), client_address)
        
        # Receive M3 from IoT device
        data, client_address = server_socket.recvfrom(config['globalVariables']['buffersize'])
        M3 = data.decode()
        logger.info(f"{client_address}: Received M3")
        M3 = Helpers.decrypt(k1,M3)
        logger.debug(f"M3 decrypted: {M3}")
        message3 = M3.split("||")
        
        # Verify the IoT devices response
        # if the IoT device uses a different k1 than the server,
        # the transmitted r1 is not the same as the the servers r1 
        if(int(message3[0])!= r1):     
            logger.error(f"{client_address}: The encryption key or r1 is not correct")
            
        else:    
            
            t1 = int(message3[1])
            message3 = message3[2][1:-1] # take away { }
            
            # Read the random number r2 and the challenge C2 from M3
            r2 = message3.split(",")[-1]
            C2 = []
            # Split off r2 and the [ ], then split for the challenge
            temp = message3[1:(message3.find(message3.split(",")[-1])-2)].split(",")    
            
            for i in temp:  # Values were transmitted as string and have to be turned back to int
                try:
                    C2.append(int(i))
                except:
                    raise ValueError("encountered ValueError while reading message3")

            # Generate encryption key k2 from the keys in the challenge C2
            # IoT device does the same on it's side 
            k2 = bytes(vault.key_length_bits) 
            for i in C2:
                k2 = Helpers.xor_bytes(k2, vault.getKey(i))
            t2 = Helpers.randInt()

            # Send M4 back to IoT device
            # M4 = Enc(k2^t1, r2||t2)
            message4 = str(r2) + "||" + str(t2)
            logger.debug(f"M4 before encrypting: {message4}")
            
            encrypt_key_M4 = Helpers.xor_bytes(k2,t1.to_bytes(64, "little"))
            
            logger.debug(f"Encryption key k2^t1: {encrypt_key_M4}")
            
            M4 = Helpers.encrypt(encrypt_key_M4, message4)
            server_socket.sendto(M4, client_address)
            logger.info(f"{client_address}: Sent M4")

            # Compute session key t
            # TESTING use for further communcation
            t = t1^t2
            logger.debug(f"t: {t}")
            

            # Change keys in vault and store them in database
            messages = M1+M2+M3+message4
            new_keys = vault.changeKeys(messages)
            logger.info("Changed keys")
            Database.store_vault_of(deviceID, new_keys)
            
    except Exception as e:
        logger.error(f"Error while handling client {client_address}: {e}")
        error = f"error: {e}"       # Sending the IoT device the exception message to inform about the server side error
        server_socket.sendto(error.encode(), client_address)

if __name__ == "__main__":
    start_server()
    
