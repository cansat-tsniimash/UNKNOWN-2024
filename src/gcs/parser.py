import sys
import argparse
import time
import struct
import datetime
import socket
import numpy as np
import ctypes

HowMuchMusor,HowMuchDefective=0,0

def DoNothing(variable):
    return variable

def crc16(data : bytearray, offset=0, length=-1):
    if length < 0:
        length = len(data)
    
    if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
        return 0

    crc = 0xFFFF
    for i in range(0, length):
        crc ^= data[offset + i] << 8
        for j in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
        crc = crc & 0xFFFF

    return crc & 0xFFFF

def generate_csv_name(text):
    now = datetime.datetime.utcnow().replace(microsecond=0)
    isostring = now.isoformat()  # string 2021-04-27T23:17:31
    isostring = isostring.replace("-", "")  # string 20210427T23:17:31
    isostring = isostring.replace(":", "")  # string 20210427T231731, òî ÷òî íàäî
    return text + isostring + ".csv"

if __name__ == '__main__':

    #filename_f = str(input("Введите имя .bin файла:"))+".bin"
    filename_f = "qwerty.bin"
    filename_f1 = generate_csv_name("./log/1_knpn")
    filename_f2 = generate_csv_name("./log/2_knpn")
    filename_f3 = generate_csv_name("./log/3_knpn")
    filename_f4 = generate_csv_name("./log/4_knpn")
    f = open(filename_f, 'rb')
    f1 = open(filename_f1, 'w')
    f1.write('"Number";"Time_ms";"Accel x";"Accel y";"Accel z";"Gyro x";"Gyro y";"Gyro z";"Mag x";"Mag y";"Mag z";"crc"\n')
    f1.flush()
    f2 = open(filename_f2, 'w')
    f2.write('"Number";"Time_ms";"Temp BME";"Pressure";"Humidity";Height BME";"Lux";"State";"crc"\n')
    f2.flush()
    f3 = open(filename_f3, 'w')
    f3.write('"Number";"Time_ms";"Fix";"Latitude";"Longitude";"Height";"Time, s";"Time, mks";"crc"\n')
    f3.flush()
    f4 = open(filename_f4, 'w')
    f4.write('"Number";"Time_ms";"Q1";"Q2";"Q3";"Q4";"Time";"crc"\n')
    f4.flush()

    while True:
        try:
            data_sir = f.read(1)
            data = np.frombuffer(data_sir, dtype=np.uint8)
        except TimeoutError:
            print("No data")

        try:
            if len(data) < 1:
                print("Наши данные иссякли")
                print("нашёл", HowMuchMusor, "лишних байтов")
                print("странных пакетов:", HowMuchDefective)
                exit()
            else:
                one = DoNothing("one")
            if data[0] == 170:
                data_sir = f.read(26)
                data_sir = bytes(range(170,171)) + data_sir
                data = np.frombuffer(data_sir, dtype=np.uint8)
    
                print("==== Пакет тип 1 ====")
                unpack_data = struct.unpack("<BHIhhhhhhhhhH", data)
                print ("Number", unpack_data[1])
                print ("Time_ms", unpack_data[2])
                print ("Accelerometer x", unpack_data[3]/1000)
                print ("Accelerometer y", unpack_data[4]/1000)
                print ("Accelerometer z", unpack_data[5]/1000)
                print ("Gyroscope x", unpack_data[6]/1000)
                print ("Gyroscope y", unpack_data[7]/1000)
                print ("Gyroscope z", unpack_data[8]/1000)
                print ("Magnetometer x", unpack_data[9]/1000)
                print ("Magnetometer y", unpack_data[10]/1000)
                print ("Magnetometer z", unpack_data[11]/1000)
                print ("crc", unpack_data[12])
                print(crc16(data[:25]))
                # print ("Number", unpack_data[2])
                # print ("Time", unpack_data[1])
                
                if crc16(data[:25])==unpack_data[12]:
                    for i in range(1,13):
                        f1.write(str(unpack_data[i]))
                        f1.write(";")
                    f1.write('\n')
                    f1.flush()
                else:
                    print("Не совпадает контрольная сумма")
                    HowMuchDefective+=1
                print ('\n')

            elif data[0] == 187:
                data_sir = f.read(25)
                data_sir = bytes(range(187,188)) + data_sir
                data = np.frombuffer(data_sir, dtype=np.uint8)

                print("==== Пакет тип 2 ====")
                unpack_data = struct.unpack("<BHIhIhffBH", data)
                print ("Number", unpack_data[1])
                print ("Time_ms", unpack_data[2])
                print ("Temperature BME", unpack_data[3]/100)
                print ("Pressure", unpack_data[4])
                print ("Humidity", unpack_data[5])
                print ("Height", unpack_data[6])
                print ("Lux", unpack_data[7])
                print ("State", unpack_data[8])
                print ("crc", unpack_data[9])
                print(crc16(data[:24]))
                # print ("Bus voltage", unpack_data[7]/1000)
                # print ("Current", unpack_data[6]/1000)
                # print ("Number", unpack_data[2])
                # print ("Photo", unpack_data[9]/100)
                # print ("State", unpack_data[8])
                # print ("Time", unpack_data[1])
                
                if crc16(data[:24])==unpack_data[9]:
                    for i in range(1,10):
                        f2.write(str(unpack_data[i]))
                        f2.write(";")
                    f2.write('\n')
                    f2.flush()
                else:
                    print("Не совпадает контрольная сумма")
                    HowMuchDefective+=1
                print ('\n')

            elif data[0] == 204:
                 data_sir = f.read(30)
                 data_sir = bytes(range(204,205)) + data_sir
                 data = np.frombuffer(data_sir, dtype=np.uint8)
                 print("==== Пакет тип 3 ====")
                 unpack_data = struct.unpack("<BHIhfffLLH", data)
                 print ("Number", unpack_data[1])
                 print ("Time_ms", unpack_data[2])
                 print ("Fix", unpack_data[3])
                 print ("Latitude", unpack_data[4])
                 print ("Longitude", unpack_data[5])
                 print ("Height", unpack_data[6])
                 print ("Time, s", unpack_data[7])
                 print ("Time, mks", unpack_data[8])
                 print ("crc", unpack_data[9])
                 print(crc16(data[:29]))
                 #print ("Number", unpack_data[2])
                 #print ("Time", unpack_data[1])
                 
                 if crc16(data[:29])==unpack_data[9]:
                    for i in range(1,10):
                        f3.write(str(unpack_data[i]))
                        f3.write(";")   
                    f3.write('\n')
                    f3.flush()
                 else:
                    print("Не совпадает контрольная сумма")
                    HowMuchDefective+=1
                 print ('\n')

            elif data[0] == 255:
                 data_sir = f.read(28)
                 data_sir = bytes(range(255,256)) + data_sir
                 data = np.frombuffer(data_sir, dtype=np.uint8)
                 print("==== Пакет тип 4 ====")
                 unpack_data = struct.unpack("<BHIfffffH", data)
                 print ("Number", unpack_data[1])
                 print ("Time_ms", unpack_data[2])
                 print ("Q1", unpack_data[4])
                 print ("Q2", unpack_data[5])
                 print ("Q3", unpack_data[6])
                 print ("Q4", unpack_data[7])
                 print ("Time", unpack_data[3])
                 print ("crc", unpack_data[8])
                 print(crc16(data[:27]))
                 
                 if crc16(data[:27])==unpack_data[8]:
                    for i in range(1,9):
                        f4.write(str(unpack_data[i]))
                        f4.write(";")    
                    f4.write('\n')
                    f4.flush()
                 else:
                    print("Не совпадает контрольная сумма")
                    HowMuchDefective+=1
                 print ('\n')
            else:
                HowMuchMusor+=1
            #time.sleep(1)
        except Exception as e:
            print(e)

        #f.write(record)
        #f.flush()
#else:
            # print('got no data')
    #pass

        #time.sleep(0.1)

