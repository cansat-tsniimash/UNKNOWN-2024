import socket
 

localIP     = "0.0.0.0"

localPort   = 20001

bufferSize  = 1024



 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setblocking(False)
UDPServerSocket.settimeout(0)
 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

 

# Listen for incoming datagrams

while(True):

    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
    
        print(clientMsg)
        print(clientIP)
        for i in range(10):
            msgFromServer       = str(i)
            bytesToSend         = str.encode(msgFromServer)
            # Sending a reply to client
            UDPServerSocket.sendto(str.encode(str(i)), address)
    except BlockingIOError as e:
        pass#print(str(e))
    except Exception as e:
        print(str(e))



