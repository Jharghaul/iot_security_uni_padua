import socket

#Create socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Destination address and port
udp_socket.bind(('localhost', 12345))

print("Waiting for data...")

while True:
    # Receive data
    data, addr = udp_socket.recvfrom(1024)
    print(f"Received data: {data.decode()}")
   

# Close the socket
print()
udp_socket.close()