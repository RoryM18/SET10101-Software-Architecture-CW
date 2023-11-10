import socket
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import threading
import time
import sqlite3

def connectToServer():
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('192.168.0.14', 12345)  # Replace with your server's IP address
            server_socket.connect(server_address)
            print("Connected to the server")
            return server_socket
        except ConnectionRefusedError:
            print("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)

clientSocket = connectToServer()

def closeClient():
    clientWindow.destroy() # Close the client window

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

    resultLabel = Label(priceControlWindow, text="")
    resultLabel.pack()

def openInventoryControlWindow():

    global resultLabel

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
        itemName = itemNameOrderEntry.get()
        quantity = quantityEntry.get()
        requestData = f"order,{itemName},{quantity}"
        clientSocket.send(requestData.encode('utf-8'))

    orderBtn = Button(inventroyControlWindow, text = "Order Stock", command = orderOutOfStockItems)
    orderBtn.pack()

    resultLabel = Label(inventroyControlWindow, text="")
    resultLabel.pack()

    def displayWarningMessage():
        requestData = "warning"
        response = clientSocket.send(requestData.encode('utf-8'))
        if response:
            tkinter.messagebox.showinfo("Warning Message", response)

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

def displayTableData():

    conn = sqlite3.connect('De_Store.db')  
    cur = conn.cursor()
    cur.execute("SELECT * FROM StoreTable")  
    data = cur.fetchall()    
    dataDisplayWindow = Toplevel(clientWindow)
    dataDisplayWindow.title("Database Data")
    dataDisplayWindow.geometry("1500x400")
    
    tree = ttk.Treeview(dataDisplayWindow, columns=("ID", "Item Name", "Stock", "Price", "Sale Offer", "Loyalty Card Iffer"))
    tree.heading("#1", text="ID")
    tree.heading("#2", text="Item Name")
    tree.heading("#3", text="Stock")
    tree.heading("#4", text="Price")
    tree.heading("#5", text="Sale Offer")
    tree.heading("#6", text="Loyalty Card Offer")
    
    tree.pack()

    for row in data:
        tree.insert("", "end", values=row)


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

closeBtn = Button(clientWindow, text="Close", command=closeClient)
closeBtn.pack(pady=10)

#Function to recieve data from server

def recieveDataFromServer():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        response = data.decode('utf-8')
        if resultLabel:
            resultLabel.config(text=response) #Update resultLable if it exists
        

#Start a seperate thread to continuously recieve data from the server
receive_thread = threading.Thread(target = recieveDataFromServer)
receive_thread.daemon = True
receive_thread.start()

#Start the Tkinter main loop
mainloop()