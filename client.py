import socket
from tkinter import *
import threading
import time

def connectToServer():
    while True:
        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            localIP = socket.gethostbyname(socket.gethostname()) #Automatically get local ip address of machine 
            serverAddress = (localIP, 12345) 
            serverSocket.connect(serverAddress)
            print("Connected to the server")
            return serverSocket
        except ConnectionRefusedError:
            print("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)

clientSocket = connectToServer()

def closeClient():
    clientWindow.destroy() # Close the client window

#Function to recieve data from server

def recieveDataFromServer():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        response = data.decode('utf-8')
        print(response)
        if resultLabel:
            resultLabel.config(text=response) #Update resultLable if it exists

#Create a Tkinter window

clientWindow = Tk()

clientWindow.title("Client")

clientWindow.geometry("500x500")

resultLabel = None

def openPriceControlWindow():

    global resultLabel

    priceControlWindow = Toplevel(clientWindow)
    priceControlWindow.title("Price Control")
    priceControlWindow.geometry("500x500")

    itemNamePriceLabel = Label(priceControlWindow, text="Item Name:")
    itemNamePriceLabel.pack()

    itemNamePriceEntry = Entry(priceControlWindow)
    itemNamePriceEntry.pack()

    newPriceLabel = Label(priceControlWindow, text="New Price:")
    newPriceLabel.pack()

    newPriceEntry = Entry(priceControlWindow)
    newPriceEntry.pack()

    newSaleLabel = Label(priceControlWindow, text="New Sale:")
    newSaleLabel.pack()

    newSaleEntry = Entry(priceControlWindow)
    newSaleEntry.pack()

    def changePrice():
        itemName = itemNamePriceEntry.get()
        newPrice = newPriceEntry.get()
        requestData = f"price,{itemName},{newPrice}"
        clientSocket.send(requestData.encode('utf-8'))

    def changeSale():
        itemName = itemNamePriceEntry.get()
        newSale = newSaleEntry.get()
        requestData = f"sale,{itemName},{newSale}"
        clientSocket.send(requestData.encode('utf-8'))

    changePriceButton = Button(priceControlWindow, text = "Change Price", command = changePrice)
    changePriceButton.pack()

    changeSaleBtn = Button(priceControlWindow, text = "Change Sale", command = changeSale)
    changeSaleBtn.pack()

    #Lable to print data received from server
    resultLabel = Label(priceControlWindow, text="")
    resultLabel.pack()

def openInventoryControlWindow():

    inventroyControlWindow = Toplevel(clientWindow)
    inventroyControlWindow.title("Inventory Control")
    inventroyControlWindow.geometry("500x500")

    itemNameOrderLabel = Label(inventroyControlWindow, text="Item Name:")
    itemNameOrderLabel.pack()

    itemNameOrderEntry = Entry(inventroyControlWindow)
    itemNameOrderEntry.pack()

    quantityLabel = Label(inventroyControlWindow, text="Item Amount To Order:")
    quantityLabel.pack()

    quantityEntry = Entry(inventroyControlWindow)
    quantityEntry.pack()

    def orderOutOfStockItems():

        global resultLabel

        itemName = itemNameOrderEntry.get()
        quantity = quantityEntry.get()
        requestData = f"order,{itemName},{quantity}"
        clientSocket.send(requestData.encode('utf-8'))

        resultLabel = Label(inventroyControlWindow, text="")
        resultLabel.pack()

    orderBtn = Button(inventroyControlWindow, text = "Order Stock", command = orderOutOfStockItems)
    orderBtn.pack()

    

    def displayWarningMessage():

        global resultLabel

        requestData = "warning"
        clientSocket.send(requestData.encode('utf-8'))

        resultLabel = Label(inventroyControlWindow, text="")
        resultLabel.pack()

        

    warningBtn = Button(inventroyControlWindow, text="Show Warning Message", command=displayWarningMessage)
    warningBtn.pack(pady=10)


def openLoyaltyCardControlWindow():

    global resultLabel

    loyaltyCardControlWindow = Toplevel(clientWindow)
    loyaltyCardControlWindow.title("Loyalty Card Control")
    loyaltyCardControlWindow.geometry("500x500")

    itemNameLoyaltyCardLabel = Label(loyaltyCardControlWindow, text="Item Name:")
    itemNameLoyaltyCardLabel.pack()

    itemNameLoyaltyCardEntry = Entry(loyaltyCardControlWindow)
    itemNameLoyaltyCardEntry.pack()

    newLoyaltyCardSaleLabel = Label(loyaltyCardControlWindow, text="New Loyalty Card Sale:")
    newLoyaltyCardSaleLabel.pack()

    newLoyaltyCardSaleEntry = Entry(loyaltyCardControlWindow)
    newLoyaltyCardSaleEntry.pack()

    def changeLoyaltyCardSale():
        itemName = itemNameLoyaltyCardEntry.get()
        newLoyaltyCardSale = newLoyaltyCardSaleEntry.get()
        requestData = f"loyalty,{itemName},{newLoyaltyCardSale}"
        clientSocket.send(requestData.encode('utf-8'))

    changeLoyaltyCardSaleBtn = Button(loyaltyCardControlWindow, text="Change Loyalty Card Sale", command=changeLoyaltyCardSale)
    changeLoyaltyCardSaleBtn.pack()

    resultLabel = Label(loyaltyCardControlWindow, text="")
    resultLabel.pack()

def openPortalWindow():
    global resultLabel

    requestData = "portal"
    clientSocket.send(requestData.encode('utf-8'))

    resultLabel = Label(clientWindow, text="")
    resultLabel.pack()


def openFinanceReportWindow():

    financeReportWindow = Toplevel(clientWindow)
    financeReportWindow.title("Finance Report")
    financeReportWindow.geometry("500x500")

    def generateReport():
        global resultLabel  
        requestData = "report"
        clientSocket.send(requestData.encode('utf-8'))
        resultLabel = Label(financeReportWindow, text="")
        resultLabel.pack(pady=100)

    generateReportBtn = Button(financeReportWindow, text="Generate Report", command=generateReport)
    generateReportBtn.pack()


def displayTableData():

    dataDisplayWindow = Toplevel(clientWindow)
    dataDisplayWindow.title("Database Data")
    dataDisplayWindow.geometry("1500x400")

    def generateDatabase():
        global resultLabel  
        requestData = "data"
        clientSocket.send(requestData.encode('utf-8'))
        resultLabel = Label(dataDisplayWindow, text="")
        resultLabel.pack(pady=100)

    showDatabaseBtn = Button(dataDisplayWindow, text="Display Database", command=generateDatabase)
    showDatabaseBtn.pack()


databaseBtn = Button(clientWindow, text = "View Database", command = displayTableData)
databaseBtn.pack(pady=10)

priceControlBtn = Button(clientWindow, text = "Open Price Control", command = openPriceControlWindow)
priceControlBtn.pack(pady=10)

inventoryControlBtn = Button(clientWindow, text = "Open Inventory Control", command = openInventoryControlWindow)
inventoryControlBtn.pack(pady=10)

loyaltyCardControlBtn = Button(clientWindow, text = "Open Loyalty Card Control", command = openLoyaltyCardControlWindow)
loyaltyCardControlBtn.pack(pady=10)

openPortalWindowBtn = Button(clientWindow, text = "Open Enabling Portal", command = openPortalWindow)
openPortalWindowBtn.pack(pady=10)

openFinanceReportBtn = Button(clientWindow, text = "Open Finance Report", command = openFinanceReportWindow)
openFinanceReportBtn.pack(pady=10)

closeBtn = Button(clientWindow, text="Close", command=closeClient)
closeBtn.pack(pady=10)


        

#Start a seperate thread to continuously recieve data from the server
receive_thread = threading.Thread(target = recieveDataFromServer)
receive_thread.daemon = True
receive_thread.start()

#Start the Tkinter main loop
mainloop()