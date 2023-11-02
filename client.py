import socket

#Create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to server

server_address = ('localhost', 12345)
client_socket.connect(server_address)

#Send data to the server

message = "Hello Server"

client_socket.send(message.encode('utf-8'))

#Recieve and print the echoed data from the server

data = client_socket.recv(1024)
print("Recieved from server: {}".format(data.decode('utf-8')))

#Clean up the connection

client_socket.close()