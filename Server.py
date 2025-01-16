import socket
import datetime
import random
import SecureVault as sv
import Helpers

Vault = sv
Vault.initialize()
sessionIds = []

#Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(Helpers.server_address)



print("Server is listening on port", Helpers.server_address[1], "...")

try:
    #Receive M1 from client
    data, client_address = server_socket.recvfrom(Helpers.buffer_size)
    message1 = data.decode()
    print(Helpers.now() + " Received M1", message1)
    message1 = message1.split("||")
    sessionIds.append(message1[1])

    #Verify deviceID
    if(message1[0]=="1337"): #TODO: check einbauen, device id nicht "hard coded", evtl irgendwo durch eine einfach Datei eine 
        # Datenbank simulueren mit "registrierten" Geräten [Prio gering:]oder direkt ne SQLite integrieren; Prio gering
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
    M2 = "{" + str(C1) + "||" + str(r1) + "}"    #TODO?: Tupel
    print(Helpers.now() + " Sent M2")
    server_socket.sendto(M2.encode(), client_address)

    #Receive M3 from client
    data, client_address = server_socket.recvfrom(Helpers.buffer_size)
    message3 = data.decode()
    print(Helpers.now() + " Received M3")
    print(message3)
    message3 = Helpers.decrypt(k1, message3)
    message3 = message3.split("||")
    print("Message3: ", message3)
    
    #Verify the IoT devices response
    if(int(message3[0])!=r1): # checks if k1 and r1 are correct
        print("not correct r1") #TODO: Error werfen
        
    else:    
        #Send M4 back to client
        #M3 = Enc(k1, r1||t1||{C2,r2})
        t1 = int(message3[1])
        message3 = message3[2][1:-1] # take a way { }
        r2 = message3.split(",")[-1]
        C2 = []
        for i in message3[1:(message3.find(message3.split(",")[-1])-2)].split(","): # white magic to split off r2 and the [ ], then split for the challenge
            C2.append(int(i))

        k2 = bytes(Vault.key_length_bits) 
        for i in C2:
            k2 = Helpers.xor_bytes(k2, Vault.getKey(i))
        t2 = random.randint(0, Helpers.randmax) # TODO move to helper?


        # Enc(k2^t1, r2||t2)
        M4 = Helpers.encrypt(Helpers.xor_bytes(k2,bytes(t1)), str(r2) + "||" + str(t2))
        server_socket.sendto(M4, client_address)
        print(Helpers.now() + " Sent M4")


except socket.error as e:   # TODO: richtiges Error Handling, feiner
    print(f"Send M4 failed: {e}")

finally:
    # Close the socket
    server_socket.close()
    print(Helpers.now() + " Server Socket was closed")
