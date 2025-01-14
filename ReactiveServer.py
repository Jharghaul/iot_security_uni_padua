import socket
import random
import SecureVault as sv
import Helpers

Vault = sv
Vault.initialize(Helpers.n)
sessionIds = []

#Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(Helpers.server_address)

def listen():
    print("Server is listening on port 12346...")
    # Maybe we want to use https://github.com/twisted/twisted for easier communication

    ### Server Reacts on the type of message
    try:
        #Receive message from client
        while(True):
            data, client_address = server_socket.recvfrom(Helpers.buffer_size)
            message = data.decode()
            print(Helpers.now() + " Received message", message)
            tmp = message.split("||")
            if(tmp[0][0] =="M"):
                message = message.split("||")
            match message[0]:
                case "M1":
                    print("M1 received")
                    key_1, r1 = handle_message_1(message[1:], client_address)
                case "M3":
                    print("M3 received")
                    handle_message_3(message[1:], client_address, key_1, r1)
                case _:
                    handle_message_3(message, client_address, key_1, r1)
                    print("Done, shutting down")
                    break


    except socket.error as e:
        print(f"Send M4 failed: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted! Cleaning up before exiting.")
        server_socket.sendto("Abort", client_address)

    finally:
        # Close the socket
        server_socket.close()
        print(Helpers.now() + " Server Socket was closed")
    

def handle_message_1(message1, client_address):
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
    M2 = "M2||" + str(C1) + "||" + str(r1)    #TODO: Tupel
    print(Helpers.now() + " Sent M2")
    server_socket.sendto(M2.encode(), client_address)
    return k1, r1


def handle_message_3(message3, client_address, k1, r1):
    #Receive M3 from client
  #  data, client_address = server_socket.recvfrom(Helpers.buffer_size)
   # message3 = data.decode()
    print(Helpers.now() + " Received M3")
    print(message3)
    message3 = Helpers.decrypt(k1, message3)
    message3 = message3.split("||")
    print("Message3: ", message3)
    
    #Verify the IoT devices response
    if(int(message3[0])!=r1): # checks if k1 and r1 are correct
        print("Captain, Captain, we need to aborrrt the mission!") # TODO be more serious
        print("sollte nicht passieren") #TODO: Verbindung mit Client schließen
        return "Error"
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
        M4 = Helpers.encrypt(Helpers.xor_bytes(k2,bytes(t1)), str(r2) + "||" + str(t2)) # "2" # TODO Enc(k2^t1, r2||t2)
        server_socket.sendto(M4, client_address)
        print(Helpers.now() + " Sent M4")



listen()