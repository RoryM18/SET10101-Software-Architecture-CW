import socket

#Create socket object

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to a specific address and port

server_address = ('localhost', 12345)
server_socket.bind(server_address)

#Listen for incoming connections

server_socket.listen(1)
print("Server is listneing on {}:{}".format(*server_address))

while True:
    #Wait for connection

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from {}:{}".format(client_address))

    #Recieve and echo back data
    
    data = client_socket.recv(1024)
    if not data:
        break
    print("Recieved: {}".format(data.decode('utf-8')))
    client_socket.send(data) #Echo the data back to the client

#Clean up the connection

client_socket.close()
server_socket.close()