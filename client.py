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
serverAddress = ('192.168.0.14', 12345)  # Replace 'server_ip_address' with the actual IP address
clientSocket.connect(serverAddress)

#Function to recieve data from server

def recieveDataFromServer():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        
def openPriceControlWindow():

    #Toplevel object which will be treated as a new window
    priceControlWindow = Toplevel(clientWindow)

    #Set the title of new window 

    priceControlWindow.title("Price Control")

    priceControlWindow.geometry("500x500")

priceControlBtn = Button(clientWindow, text="Open Price Control", command = openPriceControlWindow)

priceControlBtn.pack(pady = 10)

#Start a seperate thread to continuously recieve data from the server
receive_thread = threading.Thread(target = recieveDataFromServer)
receive_thread.daemon = True
receive_thread.start()

#Start the Tkinter main loop
mainloop()