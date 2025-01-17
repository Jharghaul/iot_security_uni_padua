import logging
import socket
import Database
import Helpers
import SecureVault as sv

Vault = sv
Vault.initialize()

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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permit reuse of the port
    server_address = (config['server']['host'], config['server']['port'])
    server_socket.bind(server_address)
    #server_socket.listen(5)     # permits just 5 connections at the same time and queues the others

    logger.info(f"Server is listening on port {config['server']['port']} ...")

    # Database initialization
    Database.create_database()

    try:
        while True:
            handle_client(server_socket)

    except Exception as e:   # TODO: richtiges Error Handling, feiner
        logger.error(f"Exchange failed: {e}")

    finally:
        # Close the socket
        server_socket.close()
        logger.info("Server Socket was closed")
        
        
def handle_client(server_socket):
    
    try:
        #Receive M1 from client
        data, client_address = server_socket.recvfrom(config['globalVariables']['buffersize'])
        M1 = data.decode()
        logger.info(f"{client_address}: Received M1")
        message1 = M1.split("||")

        #Verify deviceID
        if(Database.is_valid_device_id(message1[0])):
            logger.debug(f"{client_address}: The device is valid")
        else:
            logger.error(f"{client_address}: Error, aborting, device invalid")
            raise ValueError("Invalid device ID")
            
        #Generate a random number r1 and the challenge C1
        r1 = Helpers.randInt()
        C1 = Helpers.generateChallenge()

        # Generate key k1 from the keys in the challenge    
        k1 = bytes(Vault.key_length_bits)
        for i in C1:
            k1 = Helpers.xor_bytes(k1, Vault.getKey(i))

        #Send M2 back to client
        M2 = "{" + str(C1) + "||" + str(r1) + "}"
        logger.info(f"{client_address}: Sent M2")
        server_socket.sendto(M2.encode(), client_address)

        #Receive M3 from client
        data, client_address = server_socket.recvfrom(config['globalVariables']['buffersize'])
        M3 = data.decode()
        logger.info(f"{client_address}: Received M3")
        M3 = Helpers.decrypt(k1,M3)
        message3 = M3.split("||")
        
        #Verify the IoT devices response
        if(int(message3[0])!=r1): # checks if k1 and r1 are correct TODO: vier Augen ob das so stimmt
            logger.error(f"{client_address}: not correct r1")
            
        else:    
            #Send M4 back to client
            t1 = int(message3[1])
            message3 = message3[2][1:-1] # take away { }
            r2 = message3.split(",")[-1]
            C2 = []
            for i in message3[1:(message3.find(message3.split(",")[-1])-2)].split(","): #split off r2 and the [ ], then split for the challenge
                C2.append(int(i))

            k2 = bytes(Vault.key_length_bits) 
            for i in C2:
                k2 = Helpers.xor_bytes(k2, Vault.getKey(i))
            t2 = Helpers.randInt()


            # Enc(k2^t1, r2||t2)
            M4 = str(r2) + "||" + str(t2)
            message4 = Helpers.encrypt(Helpers.xor_bytes(k2,bytes(t1)), M4)
            server_socket.sendto(message4, client_address)
            logger.info(f"{client_address}: Sent M4")

            # compute session key t # TODO: was ist damit? erklären oder noch was damit machen
            t = t1^t2

            # Change keys in vault and close the socket
            # Vault.changeKeys(M1+M2+M3+M4) TODO: wie damit umgehen bei mehreren Client; 
            # Felix Idee: Hier Prove of Concept deklarieren und sagen dass man dafür in "further works" eine Lösung macht
    except Exception as e:
        logger.error(f"Error while handling client {client_address}: {e}")
        
        
if __name__ == "__main__":
    start_server()
    
