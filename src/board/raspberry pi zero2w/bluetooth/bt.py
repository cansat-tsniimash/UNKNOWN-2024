import socket
import time
import select

addr = '98:DA:60:0A:0E:C3'


poller = select.epoll()
sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((addr, 1))

poller.register(sock.fileno(), select.EPOLLIN | select.EPOLLERR)

while True:
	poll_rc = poller.poll()
	if poll_rc:
		data = sock.recv(4096)
		print("got data = %s" % data)

