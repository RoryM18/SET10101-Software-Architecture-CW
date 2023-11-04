import socket
import sqlite3

#Create SQLite database connection

conn = sqlite3.connect("DE_Store.db")

#Create a cursor tool to navigate the database

cur = conn.cursor()

#Create the table

table = """
    CREATE TABLE StoreTable (
        itemID INTEGER,
        itemName TEXT,
        stock INTEGER,
        price FLOAT,
        saleOffer FLOAT,
        loyaltyCardOffer FLOAT,
        primary key(itemID)
        ) """

#Execture the table

#cur.execute(table)

print("DE-Store Table Created")

items = ("Screws", 20, 3.99, 0.5, 0.10)

de_store_insert = """INSERT INTO StoreTable(itemName, stock, price, saleOffer, loyaltyCardOffer)
                     VALUES(?,?,?,?,?)"""

cur.execute(de_store_insert, items)

print("Items inserted into database")

#Commit table to the database 

#Close the connection to the database

conn.commit()
conn.close()

#Create socket object

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to a specific address and port

serverAddress = ('0.0.0.0', 12345)
serverSocket.bind(serverAddress)

#Listen for incoming connections

serverSocket.listen(1)
print("Server is listneing on {}:{}".format(*serverAddress))

while True:
    #Wait for connection

    print("Waiting for a connection...")
    clientSocket, clientAddress = serverSocket.accept()
    print("Accepted connection from {}:{}".format(*clientAddress))

    #Recieve and echo back data
    try:
        data = clientSocket.recv(1024)
        if not data:
            print("Client closed connection...")
            break #Exit loop when client closes connection
        print("Recieved: {}".format(data.decode('utf-8')))
        clientSocket.send(data) #echod data back to client
    except ConnectionResetError:
        print("Client closed connection unexpectadley")
        break

#Clean up client socket

clientSocket.close()

#Clean up server socket

serverSocket.close()        
