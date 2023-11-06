import socket
from tkinter import *
import threading
import time

def connectToServer():
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('192.168.0.183', 12345)  # Replace with your server's IP address
            server_socket.connect(server_address)
            print("Connected to the server")
            return server_socket
        except ConnectionRefusedError:
            print("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)


def closeClient():
    clientWindow.destroy() # Close the client window

#Create a Tkinter window

clientWindow = Tk()

clientWindow.title("Client")

clientWindow.geometry("500x500")

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

clientSocket = connectToServer()

priceControlBtn = Button(clientWindow, text = "Open Price Control", command = openPriceControlWindow)
priceControlBtn.pack(pady=10)

closeBtn = Button(clientWindow, text="Close", command=closeClient)
closeBtn.pack()

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