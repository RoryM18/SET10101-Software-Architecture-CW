import socket
import sqlite3
import json
import webbrowser

#Create SQLite database connection

conn = sqlite3.connect("Accounting.db")

#Create a cursor tool to navigate the database

cur = conn.cursor()

#Create the table

table = """
    CREATE TABLE FinanceTable (
        reportID INTEGER,
        month TEXT,
        numOfSales INTEGER,
        numOfDeliveries INTEGER,
        numOfReturns INTEGER,
        numOfLoyaltyCardsScanned INTEGER,
        primary key(reportID)
        ) """

#Execture the table

#cur.execute(table)

#print("Finance Table Created")

items = ("May", 923, 577, 65, 860)

accounting_insert = """INSERT INTO FinanceTable(month, numOfSales, numOfDeliveries, numOfReturns, numOfLoyaltyCardsScanned)
                     VALUES(?,?,?,?,?)"""

#cur.execute(accounting_insert, items)

#print("Items inserted into database")

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

def openHTMLportal():
    #HTML content
    htmlContent = """
    <html>
    <head><title>Enabling</title></head>
    <body>
        <h1>Welcome to Enabling</h1>
        <p>This is where the enabling system will be held</p>
    </body>
    </html>
    """

    #Save HTML content to a temporary file
    with open("enabling.html", "w") as htmlFile:
        htmlFile.write(htmlContent)

    #Open the HTML file in the default web browser
    webbrowser.open("enabling.html")


def generateReport():
    try:
        #Execute an SQL update statment to change the items sale price
        selectQuery = "SELECT * FROM FinanceTable"
        conn = sqlite3.connect("Accounting.db")
        cur = conn.cursor()
        cur.execute(selectQuery)
        data = cur.fetchall()

        reportData = []
        for row in data:
            reportData.append({
                "Month": row[1],
                "Number of Sales": row[2],
                "Number of Deliveries": row[3],
                "Number of Returns": row[4],
                "Number of Loyalty Cards Scanned": row[5]
            })

        reportJson = json.dumps(reportData)

        conn.commit()
        conn.close()
    
        return reportJson
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
            print("Received data:", requestData)
            if requestType == "price":
                response = changePrice(itemName, newValue)
            elif requestType == "sale":
                response = changeSale(itemName, newValue)
            elif requestType == "order":
                response = processOrder(itemName, newValue)
            elif requestType == "loyalty":
                response = changeloyaltySale(itemName, newValue)
            else:
                response = "Invalid request form"
        else:
            response = "Invalid request form"

        # Send the response back to the client
        clientSocket.send(response.encode('utf-8'))

        # Process the client request
        requestData = data.decode('utf-8').split(',')
        if len(requestData) == 1:
            requestType = requestData[0]
            print("Received data:", requestData)
            if requestType == "portal":
                response = openHTMLportal()
            elif requestType == "warning":
                response = warningMessage()
            elif requestType == "report":
                response = generateReport()
            else:
                response = "Invalid request form"

        clientSocket.send(response.encode('utf-8'))


    except ConnectionResetError:
        print("Client closed connection unexpectedly")
        # Clean up client socket
        break

   