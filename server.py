import socket
import sqlite3
import json

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

def changeSale(itemName, newSale):
    try:
        #Execute an SQL update statment to change the items sale price
        updateQuery = f"UPDATE storeTable SET saleOffer = '{newSale}' WHERE itemName = '{itemName}'"
        conn = sqlite3.connect("DE_Store.db")
        cur = conn.cursor()
        cur.execute(updateQuery)
        conn.commit()
        conn.close()
        return "Sale offer updated successfully."
    except sqlite3.Error as error:
        return f"Error updating sale offer: {error}"
    
def processOrder(itemName, quantity):
    try:
        updateQuery = f"UPDATE StoreTable SET stock = stock + {quantity} WHERE itemName = '{itemName}'"
        conn = sqlite3.connect("DE_Store.db")
        cur = conn.cursor()
        cur.execute(updateQuery)
        conn.commit()
        conn.close()
        return f"Ordered {quantity} {itemName} successfully."
    except sqlite3.Error as error:
        return f"Error processing order: {error}"
    
def warningMessage():
    try:
        conn = sqlite3.connect("DE_Store.db")
        cur = conn.cursor()
        
        # Select item names with stock levels less than 10
        cur.execute("SELECT itemName FROM StoreTable WHERE stock < 10")
        
        # Fetch all the results
        low_stock_items = cur.fetchall()
        
        if low_stock_items:
            # If there are items with low stock, create a warning message
            items_list = ', '.join(item[0] for item in low_stock_items)
            return f"Order more of the following items: {items_list}"
        else:
            return "No items with low stock."
    except sqlite3.Error as error:
        return f"Error generating warning message: {error}"

def changeloyaltySale(itemName, newLoyaltyCardSale):
    try:
        #Execute an SQL update statment to change the items sale price
        updateQuery = f"UPDATE storeTable SET loyaltyCardOffer = '{newLoyaltyCardSale}' WHERE itemName = '{itemName}'"
        conn = sqlite3.connect("DE_Store.db")
        cur = conn.cursor()
        cur.execute(updateQuery)
        conn.commit()
        conn.close()
        return "Loyalty Card Sale offer updated successfully."
    except sqlite3.Error as error:
        return f"Error updating sale offer: {error}"


print("Waiting for connection...")
clientSocket, clientAddress = serverSocket.accept()
print("Accepted connection from {}:{}".format(*clientAddress))

while True:

    # Receive and process data
    try:
        data = clientSocket.recv(1024)
        if not data:
            print("Client closed connection.")
            clientSocket.close()
            break

        # Process the client request
        requestData = data.decode('utf-8').split(',')
        if len(requestData) == 3:
            requestType, itemName, newValue = requestData
            if requestType == "price":
                response = changePrice(itemName, newValue)
            elif requestType == "sale":
                response = changeSale(itemName, newValue)
            elif requestType == "order":
                response = processOrder(itemName, newValue)
            elif requestType == "warning":
                response = warningMessage()
            elif requestType == "loyalty":
                response = changeloyaltySale(itemName, newValue)
            else:
                response = "Invalid request form"
        else:
            response = "Invalid request form"

        # Send the response back to the client
        clientSocket.send(response.encode('utf-8'))
    except ConnectionResetError:
        print("Client closed connection unexpectedly")
        # Clean up client socket
        break

   