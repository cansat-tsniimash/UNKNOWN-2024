import socket

 

msgFromClient       = "give me data plz"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("192.168.0.200", 20001)

bufferSize          = 1024

 

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.setblocking(False)
UDPClientSocket.settimeout(0) 

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

while(True):
	try:
		msgFromServer = UDPClientSocket.recvfrom(bufferSize)
		msg = str(msgFromServer[0])
		print(msg[2:-1])
	except BlockingIOError as e:
		pass	