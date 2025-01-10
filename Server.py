import socket
import datetime
import random
import SecureVault as sv
import Helpers

Vault = sv
Vault.initialize(Helpers.n)
sessionIds = []

#Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(Helpers.server_address)


print("Server is listening on port 12346...")
# Maybe we want to use https://github.com/twisted/twisted for easier communication

try:
    #Receive M1 from client
    data, client_address = server_socket.recvfrom(Helpers.buffer_size)
    message1 = data.decode()
    print(Helpers.now() + " Received M1", message1)
    message1 = message1.split("||")
    sessionIds.append(message1[1])

    #Verify deviceID
    if(message1[0]=="1337"): #TODO: check einbauen
        print(Helpers.now() + " The device is valid")
    else:
        print("Error, aborting, device invalid")
        #TODO: Error werfen
        
    #Generate a random number and the challenge
    r1 = random.randint(0, Helpers.randmax)
    C1 = Helpers.generateChallenge()

    # Generate key k1 from the keys in the challenge    
    k1 = bytes(Vault.key_length_bits)
    for i in C1:
        k1 = Helpers.xor_bytes(k1, Vault.getKey(i))

    #Send M2 back to client
    M2 = str(C1) + "||" + str(r1)    #TODO: Tupel
    print(Helpers.now() + " Sent M2")
    server_socket.sendto(M2.encode(), client_address)

    #Receive M3 from client
    data, client_address = server_socket.recvfrom(Helpers.buffer_size)
    message3 = data.decode()
    print(Helpers.now() + " Received M3")

    #Verify the IoT devices response

    #TODO: k1?
    #TODO: r1?

    if(False): #TODO: k1 oder r1 passen nicht?
        print("sollte nicht passieren") #TODO: Verbindung mit Client schließen
    else:    
        #Send M4 back to client
        M4 = "2" # TODO Enc(k2^t1, r2||t2)
        server_socket.sendto(M4.encode(), client_address)
        print(Helpers.now() + " Sent M4")
except socket.error as e:
    print(f"Send M4 failed: {e}")

finally:
    # Close the socket
    server_socket.close()
    print(Helpers.now() + " Server Socket was closed")
