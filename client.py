import socket
from tkinter import *
import threading

#Create a Tkinter window

clientWindow = Tk()

clientWindow.title("Client")

clientWindow.geometry("500x500")

# Create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server using the server's IP address and port
serverAddress = ('192.168.0.183', 12345)  # Replace 'server_ip_address' with the actual IP address
clientSocket.connect(serverAddress)

resultLabel = None

#Function to recieve data from server

def recieveDataFromServer():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        response = data.decode('utf-8')
        if resultLabel:
            resultLabel.config(text=response) #Update resultLable if it exists
        
def openPriceControlWindow():

    global resultLabel

    priceControlWindow = Toplevel(clientWindow)
    priceControlWindow.title("Price Control")
    priceControlWindow.geometry("500x500")

    itemNameLabel = Label(priceControlWindow, text="Item Name:")
    itemNameLabel.pack()

    itemNameEntry = Entry(priceControlWindow)
    itemNameEntry.pack()

    newPriceLabel = Label(priceControlWindow, text="New Price:")
    newPriceLabel.pack()

    newPriceEntry = Entry(priceControlWindow)
    newPriceEntry.pack()

    def changePrice():
        itemName = itemNameEntry.get()
        newPrice = newPriceEntry.get()
        requestData = f"{itemName},{newPrice}"
        clientSocket.send(requestData.encode('utf-8'))

    changePriceButton = Button(priceControlWindow, text = "Change Price", command = changePrice)
    changePriceButton.pack()

    resultLabel = Label(priceControlWindow, text="")
    resultLabel.pack()

priceControlBtn = Button(clientWindow, text = "Open Price Control", command = openPriceControlWindow)
priceControlBtn.pack(pady=10)

#Start a seperate thread to continuously recieve data from the server
receive_thread = threading.Thread(target = recieveDataFromServer)
receive_thread.daemon = True
receive_thread.start()

#Start the Tkinter main loop
mainloop()