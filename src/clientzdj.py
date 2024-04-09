import socket
import time
import struct

class Message():
	def __init__(self, message_id, source_id, msg_time, msg_data):
		self.message_id = message_id
		self.source_id = source_id
		self.data = msg_data
		self.time = msg_time
		self.creation_time = time.time()

	def get_message_id(self):
		return self.message_id

	def get_source_id(self):
		return self.source_id

	def get_time(self):
		return self.time

	def get_data_dict(self):
		return self.data

	def get_creation_time(self):
		return self.creation_time

 
class UnknownDataSource():
	def __init__(self, ServerIP="192.168.0.200", ServerPort=20001):
		self.ServerIP = ServerIP
		self.ServerPort = ServerPort

	def start(self):
		self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		self.UDPClientSocket.setblocking(False)
		self.UDPClientSocket.settimeout(0)
		self.UDPClientSocket.sendto(str.encode("Give me data plz"), (self.ServerIP, self.ServerPort))

	def read_data(self):
		try:
			msgFromServer = self.UDPClientSocket.recvfrom(1024)
			msg = str(msgFromServer)[0]
			print(msg[2:-1])
			if bytearray(msgFromServer[0])[0] == 187:
				data = struct.unpack("<BHIhIhffBH", bytearray(msgFromServer[0])[:26])
				return[Message(message_id='paket_2',
					    source_id='board',
					    msg_time = data[2],
					    msg_data= {
					    "Number": data[1],
					    "Temperature BME": data[3]/100,
					    "Pressure": data[4],
					    "Humidity": data[5],
					    "Height": data[6],
					    "Lux": data[7],
					    "State": data[8],
					    "crc": data[9]
					    })]

			elif bytearray(msgFromServer[0])[0] == 170:
				data = struct.unpack("<BHIhhhhhhhhhH", bytearray(msgFromServer[0])[:27])
				return[Message(message_id='paket_1',
						source_id='board',
						msg_time=data[2],
						msg_data= {
						"Number": data[1],
						"Accelerometer x": data[3]/1000,
						"Accelerometer y": data[4]/1000,
						"Accelerometer z": data[5]/1000,
						"Gyroscope x": data[6]/1000,
						"Gyroscope y": data[7]/1000,
						"Gyroscope z": data[8]/1000,
						"Magnetometer x": data[9]/1000,
						"Magnetometer y": data[10]/1000,
						"Magnetometer z": data[11]/1000,
						"crc": data[9]
						})]

			elif bytearray(msgFromServer[0])[0] == 204:
				data = struct.unpack("<BHIfffLLH", bytearray(msgFromServer[0])[:29])
				return[Message(message_id='paket_3',
						source_id='board',
						msg_time=data[2],
						msg_data= {
						"Number": data[1],
						"Latitude": data[3],
					 	"Longitude": data[4],
					 	"Height": data[5],
					 	"Time, s": data[6],
					 	"Time, mks": data[7],
					 	"crc": data[8]
					 	})]

			elif bytearray(msgFromServer[0])[0] == 255:
				data = struct.unpack("<BHIfffffH", bytearray(msgFromServer[0])[:29])
				return[Message(message_id='paket_4',
						source_id='board',
						msg_time=data[2],
						msg_data= {
						"Number": data[1],
						"Q1": data[4],
					 	"Q2": data[5],
					 	"Q3": data[6],
					 	"Q4": data[7],
					 	"Time": data[3],
					 	"crc": data[8]
					 	})]
		except BlockingIOError as e:
			pass
		return []

	def stop(self):
		self.UDPClientSocket.close()


data_sourse = UnknownDataSource()

data_sourse.start()


while(True):
	msg = data_sourse.read_data()
	if len(msg) > 0:
		print(msg[0].get_data_dict())

data_sourse.stop()
	