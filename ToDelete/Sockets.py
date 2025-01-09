import socket
import time

#Create socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Destination address and port
address = ('localhost', 12345)

#TODO: nur Debug-Nachricht
print("UDP socket created")

i = 1

while i < 50:
    message = str(i)
    
    try:
        udp_socket.sendto(message.encode(), address)
        i = i+1
    except socket.error as e:
        print(f"Send failed: {e}")
        
    time.sleep(5)

# Close the socket
udp_socket.close()