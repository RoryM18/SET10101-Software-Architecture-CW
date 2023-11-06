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

#cur.execute(de_store_insert, items)

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

def changePrice(itemName, newPrice):
    try:
        #Execute an SQL update statement to change the items price
        updateQuery = f"UPDATE storeTable SET price = '{newPrice}' WHERE itemName = '{itemName}'"
        conn = sqlite3.connect("DE_Store.db")
        cur = conn.cursor()
        cur.execute(updateQuery)
        conn.commit()
        conn.close()
        return "Price updated successfully."
    except sqlite3.Error as error:
        return f"Error updating price: {error}"

while True:

    print("Waiting for connection...")

    clientSocket, clientAddress = serverSocket.accept()
    print("Accepted connection from {}:{}".format(*clientAddress))

    #Recieve and echo back data
    try:
        data = clientSocket.recv(1024)
        if not data:
            print("Client closed connection.")
            clientSocket.close() #Close the client socket, not the server socket

        #Process the client request to change the price

        requestData = data.decode('utf-8').split(',')
        if len(requestData) == 2:
            itemName, newPrice = requestData
            response = changePrice(itemName, newPrice)
        else:
            response = "Invalid request form."

        #Send the response back to the client

        clientSocket.send(response.encode('utf-8'))
    except ConnectionResetError:
        print("Client closed connection unexpectedly")
        break

    #Clean up client socket

    clientSocket.close()    
