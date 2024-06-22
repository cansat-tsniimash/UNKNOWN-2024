#!/usr/bin/python3
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from sys import argv, exit, stdout
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from source.main_window import MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
import os
import math
import time
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import pyquaternion
import datetime
from math import *
from stl import mesh
from itertools import chain
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import ctypes

import socket
import struct








#f_quat = open('quat.txt', 'w+')
#f_quat.write('hi')
#f_quat.write('hi')

#txt = f_quat.read()
#print(txt)
#print(1)

#with open('testFile.bin', 'rb') as file_telem:
now_str = datetime.datetime.now().replace(microsecond=0).isoformat().replace(":", "-")
tlm_base_path = "telemetry\\"
os.makedirs(tlm_base_path, exist_ok=True)

file_telem = open('testFile.bin', 'rb')

file_acc = open(tlm_base_path + 'file_acc-' + now_str + '.txt', 'w+')
file_mag = open(tlm_base_path + 'file_mag-' + now_str + '.txt', 'w+')
file_p1 = open(tlm_base_path + 'file_p1-' + now_str + '.txt', 'w+')
file_p1.write("Номер пакета")
file_p1.write('\t')
file_p1.write("Время")
file_p1.write('\t')
file_p1.write("Давление")
file_p1.write('\t')
file_p1.write("Температура")
file_p1.write('\t')
file_p1.write("Высота")
file_p1.write('\t')
file_p1.write("Состояние")
file_p1.write('\n')
file_p1.flush()
file_p12 = open(tlm_base_path + 'file_p12-' + now_str + '.txt', 'w+')
file_p12.write("Номер пакета")
file_p12.write('\t')
file_p12.write("Время")
file_p12.write('\t')
file_p12.write("Широта")
file_p12.write('\t')
file_p12.write("Долгота")
file_p12.write('\t')
file_p12.write("Высота")
file_p12.write('\t')
file_p12.write("fix GPS")
file_p12.write('\n')
file_p12.flush()
file_p2 = open(tlm_base_path + 'file_p2-' + now_str + '.txt', 'w+')
file_p2.write("Номер пакета")
file_p2.write('\t')
file_p2.write("Время")
file_p2.write('\t')
file_p2.write("acc_X")
file_p2.write('\t')
file_p2.write("acc_Y")
file_p2.write('\t')
file_p2.write("acc_Z")
file_p2.write('\t')
file_p2.write("gyro_X")
file_p2.write('\t')
file_p2.write("gyro_Y")
file_p2.write('\t')
file_p2.write("gyro_Z")
file_p2.write('\t')
file_p2.write("mag_X")
file_p2.write('\t')
file_p2.write("mag_Y")
file_p2.write('\t')
file_p2.write("mag_Z")
file_p2.write('\t')
file_p2.write("q0")
file_p2.write('\t')
file_p2.write("q1")
file_p2.write('\t')
file_p2.write("q2")
file_p2.write('\t')
file_p2.write("q3")
file_p2.write('\t')
file_p2.write("q4")
file_p2.write('\t')
file_p2.write("Лидар")
file_p2.write('\n')
file_p2.flush()
file_points = open(tlm_base_path + 'file_points-' + now_str + '.txt', 'w+')
file_points.write("Время")
file_points.write("\t")
file_points.write("X")
file_points.write("\t")
file_points.write("Y")
file_points.write("\t")
file_points.write("Z")
file_points.write("\n")
file_points.flush()
file_p1_raw = open(tlm_base_path + 'file_p1_raw-' + now_str + '.txt', 'w+')
file_p1_raw.write("Номер пакета")
file_p1_raw.write('\t')
file_p1_raw.write("Время")
file_p1_raw.write('\t')
file_p1_raw.write("Давление")
file_p1_raw.write('\t')
file_p1_raw.write("Температура")
file_p1_raw.write('\t')
file_p1_raw.write("Высота")
file_p1_raw.write('\t')
file_p1_raw.write("Состояние")
file_p1_raw.write('\n')
file_p1_raw.flush()
file_p12_raw = open(tlm_base_path + 'file_p12_raw-' + now_str + '.txt', 'w+')
file_p12_raw.write("Номер пакета")
file_p12_raw.write('\t')
file_p12_raw.write("Время")
file_p12_raw.write('\t')
file_p12_raw.write("Широта")
file_p12_raw.write('\t')
file_p12_raw.write("Долгота")
file_p12_raw.write('\t')
file_p12_raw.write("Высота")
file_p12_raw.write('\t')
file_p12_raw.write("fix GPS")
file_p12_raw.write('\n')
file_p12_raw.flush()
file_p2_raw = open(tlm_base_path + 'file_p2_raw-' + now_str + '.txt', 'w+')
file_p2_raw.write("Номер пакета")
file_p2_raw.write('\t')
file_p2_raw.write("Время")
file_p2_raw.write('\t')
file_p2_raw.write("acc_X")
file_p2_raw.write('\t')
file_p2_raw.write("acc_Y")
file_p2_raw.write('\t')
file_p2_raw.write("acc_Z")
file_p2_raw.write('\t')
file_p2_raw.write("gyro_X")
file_p2_raw.write('\t')
file_p2_raw.write("gyro_Y")
file_p2_raw.write('\t')
file_p2_raw.write("gyro_Z")
file_p2_raw.write('\t')
file_p2_raw.write("mag_X")
file_p2_raw.write('\t')
file_p2_raw.write("mag_Y")
file_p2_raw.write('\t')
file_p2_raw.write("mag_Z")
file_p2_raw.write('\t')
file_p2_raw.write("Лидар")
file_p2_raw.write('\n')
file_p2_raw.flush()




coordinate = np.array([])


pg.setConfigOption('background', '#646464')
pg.setConfigOption('foreground', '#ffffff')


MESH_PATH = os.path.abspath('Sat_Simple2.stl')

# print("Укажите с какой частотой обновлять графики в секундах:")
N = float(sys.argv[1])
Count1 = 0
Count12 = 0
Count2 = 0

t = time.time()
timer = time.time() - t

time_pr1 = 0
time_p1 = 0
time_pr12 = 0
time_p12 = 0
time_pr2 = 0
time_p2 = 0
dt1 = 0
dt12 = 0
dt2 = 0


class packet_ma_type_11_t(ctypes.Structure):
    _fields_ = [('flag', ctypes.c_uint8),
                ('num', ctypes.c_uint16),
                ('time', ctypes.c_uint32),
                ('BME280_pressure', ctypes.c_double),
                ('BME280_temperature', ctypes.c_float),
                ('height_bme', ctypes.c_double),
                ('state', ctypes.c_uint8), 
                ('sum', ctypes.c_uint16)]

class packet_ma_type_12_t(ctypes.Structure):
    _fields_ = [('flag', ctypes.c_uint8),
                ('num', ctypes.c_uint16),
                ('time', ctypes.c_uint32),
                ('latitude', ctypes.c_float),
                ('longitude', ctypes.c_float),
                ('altitude', ctypes.c_float),
                ('fix', ctypes.c_uint8), 
                ('volts', ctypes.c_float),
                ('lux', ctypes.c_float),
                ('sum', ctypes.c_uint16),
                ('null', ctypes.c_uint8 * 2)]

class packet_ma_type_2_t(ctypes.Structure):
    _fields_ = [('flag', ctypes.c_uint8),
                ('num', ctypes.c_uint16),
                ('time', ctypes.c_uint32),
                ('acc_mg', ctypes.c_int16 * 3),
                ('gyro_mdps', ctypes.c_int16 * 3),
                ('LIS3MDL_magnetometer', ctypes.c_int16 * 3),
                ('lidar', ctypes.c_uint16), 
                ('sum', ctypes.c_uint16)]
##################################NEW
class new_packet_ma_type_11_t(ctypes.Structure):
    _fields_ = [('num', ctypes.c_uint16),
                ('time', ctypes.c_float),
                ('BME280_pressure', ctypes.c_double),
                ('BME280_temperature', ctypes.c_float),
                ('height_bme', ctypes.c_double),
                ('state', ctypes.c_uint8)]
                

class new_packet_ma_type_12_t(ctypes.Structure):
    _fields_ = [('num', ctypes.c_uint16),
                ('time', ctypes.c_float),
                ('latitude', ctypes.c_float),
                ('longitude', ctypes.c_float),
                ('altitude', ctypes.c_float),
                ('fix', ctypes.c_uint8),
                ('volts', ctypes.c_float),
                ('lux', ctypes.c_float)]

                

class new_packet_ma_type_2_t(ctypes.Structure):
    _fields_ = [('num', ctypes.c_uint16),
                ('time', ctypes.c_float),
                ('acc_mg', ctypes.c_float * 3),
                ('gyro_mdps', ctypes.c_float * 3),
                ('LIS3MDL_magnetometer', ctypes.c_float * 3),
                ('lidar', ctypes.c_double),
                ('q', ctypes.c_float * 4)]
#class coordinate_t(ctypes.Structure):
#    _fields_ = [('time', ctypes.c_float),
#                ('x_lat', ctypes.c_float),
#                ('y_lon', ctypes.c_float),
#                ('z_bme', ctypes.c_float)]


class point_t(ctypes.Structure):
    _fields_ = [('time', ctypes.c_float),
                ('x', ctypes.c_float),
                ('y', ctypes.c_float),
                ('z', ctypes.c_float)]
class pointArray_t(ctypes.Structure):
    _fields_ = [('pointArray', point_t * 10)]



def makeData():
    x = np.random.rand(1000) * 20.0 - 10.0
    y = np.random.rand(len(x)) * 20.0 - 10.0

    z = np.sin(x * 0.3) * np.cos(y * 0.75)
    return x, y, z


class DataManager(QtCore.QObject):
    new_data_p1 = QtCore.pyqtSignal(list)
    new_data_p12 = QtCore.pyqtSignal(list)
    new_data_p2 = QtCore.pyqtSignal(list)
    mutex = QtCore.QMutex()
    #autoclose = QtCore.pyqtSignal(str)
    #finished = QtCore.pyqtSignal

    #def __init__(self, ServerIP="192.168.0.200", ServerPort=6041):
    #    super(DataManager, self).__init__()
    #    self.ServerIP = ServerIP
    #    self.ServerPort = ServerPort

    def start(self):
        self.bufferSize = 32
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.setblocking(False)
        self.UDPClientSocket.settimeout(1)
        #self.UDPClientSocket.sendto(str.encode("Give me data plz"), (self.ServerIP, self.ServerPort))
          
        self.lib1 = ctypes.CDLL("func_de_la_function/func_de_la_function/libtest.dll")    

        self.lib1.MadgwickAHRSupdate.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float)
        self.lib1.MadgwickAHRSupdate.restype = ctypes.c_void_p

        self.lib1.lsm6ds3_from_fs16g_to_mpss.argtypes = [ctypes.c_int16]
        self.lib1.lsm6ds3_from_fs16g_to_mpss.restype = ctypes.c_float

        self.lib1.lsm6ds3_from_fs2000dps_to_degps.argtypes = [ctypes.c_int16]
        self.lib1.lsm6ds3_from_fs2000dps_to_degps.restype = ctypes.c_float

        self.lib1.lis3mdl_from_fs16_to_gauss.argtypes = [ctypes.c_int16]
        self.lib1.lis3mdl_from_fs16_to_gauss.restype = ctypes.c_float

        self.lib1.pars_p11.argtypes = [ctypes.POINTER(packet_ma_type_11_t), ctypes.POINTER(new_packet_ma_type_11_t)]
        self.lib1.pars_p12.argtypes = [ctypes.POINTER(packet_ma_type_12_t), ctypes.POINTER(new_packet_ma_type_12_t)]
        self.lib1.pars_2.argtypes = [ctypes.POINTER(packet_ma_type_2_t), ctypes.POINTER(new_packet_ma_type_2_t), ctypes.c_float]

        self.lib1.GetCoordinates.argtypes = [ctypes.POINTER(new_packet_ma_type_11_t), ctypes.POINTER(new_packet_ma_type_12_t), ctypes.POINTER(new_packet_ma_type_2_t), ctypes.POINTER(pointArray_t), ctypes.c_int]
        self.lib1.GetCoordinates.restypes = ctypes.c_int
        print("UDP server up and listening")

#Парсинг пакетов
    def run(self):
        #global f_quat

        global file_acc
        global file_mag
        global time_pr1
        global time_p1
        global time_pr12
        global time_p12
        global time_pr2
        global time_p2
        global dt1
        global dt12
        global dt2

        global N
        #global Count1
        #global Count12
        #global Count2

        new_packet_ma_type_11 = new_packet_ma_type_11_t()
        new_packet_ma_type_12 = new_packet_ma_type_12_t()
        new_packet_ma_type_2 = new_packet_ma_type_2_t()
        point = point_t()
        pointArray = pointArray_t()
        self.mutex.lock()
        self.close_flag = 0
        self.mutex.unlock()
        self.start()
        p1_portion = []
        p2_portion = []
        p3_portion = []
        emit_deadline = time.time() + 0.1
        p1_lst = []
        p12_lst = []
        p2_lst = []

        start_time = time.time()
        while True:

            self.mutex.lock()
            if self.close_flag == 1:
                self.mutex.unlock()
                break
            self.mutex.unlock()
            
            # Bind to address and ip
            try:
                #with open('testFile.bin', 'rb') as file_telem:
                data_sir = file_telem.read(32)
                data = np.frombuffer(data_sir, dtype=np.uint8)
                print(*data, '\n')
                #print(222)
            except TimeoutError:
                print("No data")
                continue
            #print(data[0])

            if data[0] == 0xff:
                #print(1111111111111111111111111111111111111111111111111111111111111111)
                pack = struct.unpack("<BHLdfdBHBB", data)
                #print(data[0])
                packet_ma_type_11 = packet_ma_type_11_t(pack[0], pack[1], pack[2], pack[3], pack[4], pack[5], pack[6], pack[7])
                new_packet_ma_type_11 = new_packet_ma_type_11_t()

                time_pr1 = time_p1
                time_p1 = packet_ma_type_11.time
                dt1 = time_p1 - time_pr1
                #print(time_pr1)
                #print(time_p1)
                #print(dt1)

                self.lib1.pars_p11(ctypes.pointer(packet_ma_type_11), ctypes.pointer(new_packet_ma_type_11))
                #print("num:", new_packet_ma_type_11.num)
                #print(new_packet_ma_type_11)
                #print("time:", new_packet_ma_type_11.time)
                #print("bme_press:", new_packet_ma_type_11.BME280_pressure)
                #print("bme_temperature:", new_packet_ma_type_11.BME280_temperature)
                #print("bme_height:", new_packet_ma_type_11.height_bme)
                #print("state:", new_packet_ma_type_11.state)
                #print("num:", packet_ma_type_11.num)
                #print(packet_ma_type_11)
                #print("time:", packet_ma_type_11.time)
                #print("bme_press:", packet_ma_type_11.BME280_pressure)
                #print("bme_temperature:", packet_ma_type_11.BME280_temperature)
                #print("bme_height:", packet_ma_type_11.height_bme)

                #Count1 += 1

                file_p1_raw.write(str(packet_ma_type_11.num))
                file_p1_raw.write('\t')
                file_p1_raw.write(str(packet_ma_type_11.time))
                file_p1_raw.write('\t')
                file_p1_raw.write(str(packet_ma_type_11.BME280_pressure))
                file_p1_raw.write('\t')
                file_p1_raw.write(str(packet_ma_type_11.BME280_temperature))
                file_p1_raw.write('\t')
                file_p1_raw.write(str(packet_ma_type_11.height_bme))
                file_p1_raw.write('\t')
                file_p1_raw.write(str(packet_ma_type_11.state))
                file_p1_raw.write('\n')
                file_p1_raw.flush()

                file_p1.write(str(new_packet_ma_type_11.num))
                file_p1.write('\t')
                file_p1.write(str(new_packet_ma_type_11.time))
                file_p1.write('\t')
                file_p1.write(str(new_packet_ma_type_11.BME280_pressure))
                file_p1.write('\t')
                file_p1.write(str(new_packet_ma_type_11.BME280_temperature))
                file_p1.write('\t')
                file_p1.write(str(new_packet_ma_type_11.height_bme))
                file_p1.write('\t')
                file_p1.write(str(new_packet_ma_type_11.state))
                file_p1.write('\n')
                file_p1.flush()



                p1_lst.append(new_packet_ma_type_11)
                #self.new_data_p1.emit(new_packet_ma_type_11)







            if data[0] == 0xfa:
                #print(11111111111111111111111111112222222222222222222222222222222222)
                print(data[0])
                pack = struct.unpack("<BHL3fB2fH2B", data)
                #print(data[0])
                packet_ma_type_12 = packet_ma_type_12_t(pack[0], pack[1], pack[2], pack[3], pack[4], pack[5], pack[6], pack[7], pack[8], pack[9])
                new_packet_ma_type_12 = new_packet_ma_type_12_t()

                time_pr12 = time_p12
                time_p12 = packet_ma_type_12.time
                dt12 = time_p12 - time_pr12
                #print(dt12)

                self.lib1.pars_p12(ctypes.pointer(packet_ma_type_12), ctypes.pointer(new_packet_ma_type_12))
                #print("num:", new_packet_ma_type_12.num)
                #print("time:", new_packet_ma_type_12.time)
                #print("latitude:", new_packet_ma_type_12.latitude)
                #print("longitude:", new_packet_ma_type_12.longitude)
                print("altitude:", new_packet_ma_type_12.altitude)
                #print("fix:", new_packet_ma_type_12.fix)
                #print("volts:", new_packet_ma_type_12.volts)
                #print("lux:", new_packet_ma_type_12.lux)
                #print("num:", packet_ma_type_12.num)
                #print("time:", packet_ma_type_12.time)
                #print("latitude:", packet_ma_type_12.latitude)
                #print("longitude:", packet_ma_type_12.longitude)
                #print("altitude:", packet_ma_type_12.altitude)
                #print("fix:", packet_ma_type_12.fix)

                #Count12 += 1

                file_p12_raw.write(str(packet_ma_type_12.num))
                file_p12_raw.write('\t')
                file_p12_raw.write(str(packet_ma_type_12.time))
                file_p12_raw.write('\t')
                file_p12_raw.write(str(packet_ma_type_12.latitude))
                file_p12_raw.write('\t')
                file_p12_raw.write(str(packet_ma_type_12.longitude))
                file_p12_raw.write('\t')
                file_p12_raw.write(str(packet_ma_type_12.altitude))
                file_p12_raw.write('\t')
                file_p12_raw.write(str(packet_ma_type_12.fix))
                file_p12_raw.write('\n')
                file_p12_raw.flush()

                file_p12.write(str(new_packet_ma_type_12.num))
                file_p12.write('\t')
                file_p12.write(str(new_packet_ma_type_12.time))
                file_p12.write('\t')
                file_p12.write(str(new_packet_ma_type_12.latitude))
                file_p12.write('\t')
                file_p12.write(str(new_packet_ma_type_12.longitude))
                file_p12.write('\t')
                file_p12.write(str(new_packet_ma_type_12.altitude))
                file_p12.write('\t')
                file_p12.write(str(new_packet_ma_type_12.fix))
                file_p12.write('\n')
                file_p12.flush()

                p12_lst.append(new_packet_ma_type_12)
                #self.new_data_p12.emit(new_packet_ma_type_12)
                


            if data[0] == 0xaa:
                #print(2222222222222222222222222222222222222222222222222222222222222222222)
                pack = struct.unpack("<BHL9h2H3B", data)
                #print(data[0])
                packet_ma_type_2 = packet_ma_type_2_t()

                
                packet_ma_type_2.flag = pack[0]
                packet_ma_type_2.num = pack[1]
                packet_ma_type_2.time = pack[2]
                packet_ma_type_2.acc_mg[0] = pack[3]
                packet_ma_type_2.acc_mg[1] = pack[4]
                packet_ma_type_2.acc_mg[2] = pack[5]
                #print(packet_ma_type_2.acc_mg[0])
                #print(packet_ma_type_2.acc_mg[1])
                #print(packet_ma_type_2.acc_mg[2])
                packet_ma_type_2.gyro_mdps[0] = pack[6]
                packet_ma_type_2.gyro_mdps[1] = pack[7]
                packet_ma_type_2.gyro_mdps[2] = pack[8]
                #g1 = packet_ma_type_2.gyro_mdps[0]*70.0/1000.0
                #packet_ma_type_2.gyro_mdps[0] = int(g1/70.0*1000.0)
                #g2 = packet_ma_type_2.gyro_mdps[1]*70.0/1000.0 + 3.5
                #packet_ma_type_2.gyro_mdps[1] = int(g2/70.0*1000.0)
                #g3 = packet_ma_type_2.gyro_mdps[2]*70.0/1000.0 + 1.7
                #packet_ma_type_2.gyro_mdps[2] = int(g3/70.0*1000.0)


                time_pr2 = time_p2
                time_p2 = packet_ma_type_2.time
                dt2 = time_p2 - time_pr2
                #print(dt2)


                packet_ma_type_2.LIS3MDL_magnetometer[0] = pack[9]
                packet_ma_type_2.LIS3MDL_magnetometer[1] = pack[10]
                packet_ma_type_2.LIS3MDL_magnetometer[2] = pack[11]
                packet_ma_type_2.lidar = pack[12]
                packet_ma_type_2.sum = pack[13]
                new_packet_ma_type_2 = new_packet_ma_type_2_t()

                #print(time_pr)


                self.lib1.pars_2(ctypes.pointer(packet_ma_type_2), ctypes.pointer(new_packet_ma_type_2), time_pr2)
                #print("num:", new_packet_ma_type_2.num)
                #print("time:", new_packet_ma_type_2.time)
                #print("acc1:", new_packet_ma_type_2.acc_mg[0])
                #print("acc2:", new_packet_ma_type_2.acc_mg[1])
                #print("acc3:", new_packet_ma_type_2.acc_mg[2])
                #print("gyro_mdps1:", new_packet_ma_type_2.gyro_mdps[0])
                #print("gyro_mdps2:", new_packet_ma_type_2.gyro_mdps[1])
                #print("gyro_mdps3:", new_packet_ma_type_2.gyro_mdps[2])
                #print("LIS3MDL_magnetometer1:", new_packet_ma_type_2.LIS3MDL_magnetometer[0])
                #print("LIS3MDL_magnetometer2:", new_packet_ma_type_2.LIS3MDL_magnetometer[1])
                #print("LIS3MDL_magnetometer3:", new_packet_ma_type_2.LIS3MDL_magnetometer[2])
                #print("lidar:", new_packet_ma_type_2.lidar)
                #print("q0", new_packet_ma_type_2.q[0])
                #print("q1", new_packet_ma_type_2.q[1])
                #print("q2", new_packet_ma_type_2.q[2])
                #print("q3", new_packet_ma_type_2.q[3])

                file_p2_raw.write(str(packet_ma_type_2.num))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.time))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.acc_mg[0]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.acc_mg[1]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.acc_mg[2]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.gyro_mdps[0]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.gyro_mdps[1]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.gyro_mdps[2]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.LIS3MDL_magnetometer[0]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.LIS3MDL_magnetometer[1]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.LIS3MDL_magnetometer[2]))
                file_p2_raw.write('\t')
                file_p2_raw.write(str(packet_ma_type_2.lidar))
                file_p2_raw.write('\n')
                file_p2_raw.flush()



                file_p2.write(str(new_packet_ma_type_2.num))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.time))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.acc_mg[0]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.acc_mg[1]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.acc_mg[2]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.gyro_mdps[0]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.gyro_mdps[1]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.gyro_mdps[2]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[0]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[1]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[2]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.lidar))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.q[0]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.q[1]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.q[2]))
                file_p2.write('\t')
                file_p2.write(str(new_packet_ma_type_2.q[3]))
                file_p2.write('\n')
                file_p2.flush()



                file_acc.write(str(new_packet_ma_type_2.acc_mg[0]))
                file_acc.write('\t')
                file_acc.write(str(new_packet_ma_type_2.acc_mg[1]))
                file_acc.write('\t')
                file_acc.write(str(new_packet_ma_type_2.acc_mg[2]))
                file_acc.write('\n')
                file_acc.flush()
                file_mag.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[0]))
                file_mag.write('\t')
                file_mag.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[1]))
                file_mag.write('\t')
                file_mag.write(str(new_packet_ma_type_2.LIS3MDL_magnetometer[2]))
                file_mag.write('\n')
                file_mag.flush()

                #f_quat.write(str(new_packet_ma_type_2.q[0]))
                #f_quat.write(str(new_packet_ma_type_2.q[1]))
                #f_quat.write(str(new_packet_ma_type_2.q[2]))
                #f_quat.write(str(new_packet_ma_type_2.q[3]))
                #f_quat.write('hi')
                #f_quat.write('/n')
                #print("here")



                #print("num:", packet_ma_type_2.num)
                #print("time:", packet_ma_type_2.time)
                #accc1 = packet_ma_type_2.acc_mg[0] * 488.0/1000.0/1000.0 * 9.8
                #accc2 = packet_ma_type_2.acc_mg[1] * 488.0/1000.0/1000.0 * 9.8
                #accc3 = packet_ma_type_2.acc_mg[2] * 488.0/1000.0/1000.0 * 9.8
                #print(accc3)
                #new_packet_ma_type_2.gyro_mdps[0] = packet_ma_type_2.gyro_mdps[0] *70.0/1000.0
                #new_packet_ma_type_2.gyro_mdps[1] = packet_ma_type_2.gyro_mdps[1] *70.0/1000.0
                #new_packet_ma_type_2.gyro_mdps[2] = packet_ma_type_2.gyro_mdps[2] *70.0/1000.0

                #new_packet_ma_type_2.LIS3MDL_magnetometer[0] = packet_ma_type_2.LIS3MDL_magnetometer[0] / 1711.0
                #new_packet_ma_type_2.LIS3MDL_magnetometer[1] = packet_ma_type_2.LIS3MDL_magnetometer[1] / 1711.0
                #new_packet_ma_type_2.LIS3MDL_magnetometer[2] = packet_ma_type_2.LIS3MDL_magnetometer[2] / 1711.0


                #new_packet_ma_type_2.acc_mg[0] = accc1
                #new_packet_ma_type_2.acc_mg[1] = accc2
                #new_packet_ma_type_2.acc_mg[2] = accc3

                #print("acc1:", accc1)
                #print("acc1:", packet_ma_type_2.acc_mg[0])
                #print("acc2:", accc2)
                #print("acc3:", accc3)
                #print("gyro_mdps1:", packet_ma_type_2.gyro_mdps[0])
                #print("gyro_mdps2:", packet_ma_type_2.gyro_mdps[1])
                #print("gyro_mdps3:", packet_ma_type_2.gyro_mdps[2])
                #print("LIS3MDL_magnetometer1:", packet_ma_type_2.LIS3MDL_magnetometer[0])
                #print("LIS3MDL_magnetometer2:", packet_ma_type_2.LIS3MDL_magnetometer[1])
                #print("LIS3MDL_magnetometer3:", packet_ma_type_2.LIS3MDL_magnetometer[2])
                #print("lidar:", packet_ma_type_2.lidar)

                #Count2 += 1
                p2_lst.append(new_packet_ma_type_2)
                #self.new_data_p2.emit(new_packet_ma_type_2)


            arr_len = self.lib1.GetCoordinates(ctypes.pointer(new_packet_ma_type_11), ctypes.pointer(new_packet_ma_type_12), ctypes.pointer(new_packet_ma_type_2), ctypes.pointer(pointArray), 10)
            print("Points_len:", arr_len)
            for i in range(arr_len):
                P_time = pointArray.pointArray[i].time
                x = pointArray.pointArray[i].x
                y = pointArray.pointArray[i].y
                z = pointArray.pointArray[i].z
                print("Points_arr", P_time, x, y, z)
                file_points.write(str(P_time))
                file_points.write("\t")
                file_points.write(str(x))
                file_points.write("\t")
                file_points.write(str(y))
                file_points.write("\t")
                file_points.write(str(z))
                file_points.write("\n")
                file_points.flush()

            

            #for i in range(arr_len):



            #Эмит пакетов каждые N секунд
            if time.time() - start_time > N:
                self.new_data_p1.emit(p1_lst)
                self.new_data_p12.emit(p12_lst)
                self.new_data_p2.emit(p2_lst)

                start_time = time.time()
                p1_lst = []
                p12_lst = []
                p2_lst = []
#


            

    def finish(self):
        self.mutex.lock()
        self.close_flag = 1
        self.mutex.unlock()
        self.UDPClientSocket.close()



class TopData():
    def makeData():
        x = np.random.rand(1000) * 20.0 - 10.0
        y = np.random.rand(len(x)) * 20.0 - 10.0

        z = np.sin(x * 0.3) * np.cos(y * 0.75)
        return x, y, z






#Функция обновления графиков
def add_data_to_plot(curve, x, y, limit=100):
    data = curve.getData()
    dlen = len(x)
    if len(curve.getData()[0]) + 1 > limit:
        curve.setData(np.append(curve.getData()[0][dlen:], x), np.append(curve.getData()[1][dlen:], y))
    else:
        curve.setData(np.append(curve.getData()[0], x), np.append(curve.getData()[1], y))
#




#Создание класса 3д отображения аппарата
class PlaneWidget(gl.GLViewWidget):
    def __init__(self, mesh_path, *args, **kwargs):
        super(PlaneWidget, self).__init__(*args, **kwargs)
        self.setCameraPosition(distance=13)
        self.setBackgroundColor([100, 100, 100, 0])
        g = gl.GLGridItem()
        self.addItem(g)

        isc_coord = gl.GLAxisItem()
        isc_coord.setSize(100, 100, 100)
        self.addItem(isc_coord)

        self.plane_axis = gl.GLAxisItem()
        self.plane_axis.setSize(x=300, y=300, z=300)
        self.addItem(self.plane_axis)

        verts = self._get_mesh_points(mesh_path)

        faces = np.array([(i, i + 1, i + 2,) for i in range(0, len(verts), 3)])
        colors = np.array([(1.0, 1.0, 0.0, 1.0,) for i in range(0, len(verts), 3)])
        self.mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False, shader='shaded')

        #self.mesh.rotate(180, 0, 0, 1)

        self.addItem(self.mesh)
        # self._update_mesh([0, 0, 1])

    def on_new_records(self, records):
        self._update_mesh(records)

    def _get_mesh_points(self, mesh_path):
        your_mesh = mesh.Mesh.from_file(mesh_path)
        points = your_mesh.points

        points = np.array(list(chain(*points)))
        i = 0
        nd_points = np.ndarray(shape=(len(points) // 3, 3,))
        for i in range(0, len(points) // 3):
            nd_points[i] = points[i * 3: (i + 1) * 3]

        return nd_points

    def _transform_object(self, target, move=True, rotate=True, scale=1):
        target.resetTransform()
        target.scale(scale, scale, scale)
        if move: target.translate(0, 0, 0.1)
        if rotate:
            target.rotate(degrees(self.rotation.angle), self.rotation.axis[0], self.rotation.axis[1],
                          self.rotation.axis[2])

    def _update_rotation(self, record):
        quat = pyquaternion.Quaternion(record)
        self.rotation = quat

        self._transform_object(self.mesh, move=False)

        self._transform_object(self.plane_axis, move=False)
#



#Создание массивов телеметрии
a = time.time()
arr_p1 = np.array([])
arr_p12 = np.array([])
arr_p2 = np.array([])
#


#Создание окна программы и работа в программы          
class App(QWidget):
    global Count1
    global Count12
    global Count2
    def __init__(self):



        super(App, self).__init__()
        global a
        Form, Baze = uic.loadUiType('GroundMain.ui')
        self.ui = Form()
        self.ui.setupUi(self)
        self.data_thread = QtCore.QThread(self)
        self.data_object = DataManager()
        self.data_object.moveToThread(self.data_thread)
        self.data_thread.started.connect(self.data_object.run)
        self.data_thread.start()
        self.data_object.new_data_p1.connect(self.new_data_reaction_p1)
        self.data_object.new_data_p12.connect(self.new_data_reaction_p12)
        self.data_object.new_data_p2.connect(self.new_data_reaction_p2)
        self.new_curve_p1 = True
        self.new_curve_p12 = True
        self.new_curve_p2 = True
        self.Orient = PlaneWidget(MESH_PATH)
        #self.Orient.setSizePolicy(QSizePolicy.Expanding)
        #self.Orient.setSizePolicy(self, self.sizePolicy.Minimum , self.sizePolicy.Expanding)
        self.ui.verticalLayout_8.addWidget(self.Orient)




        x, y, z = TopData.makeData()
        Top = QWidget(self)

        Top.setStyleSheet('background-color:#646464;')

        #Создание экземпляра объекта Figure из matplotlib
        self.figure = Figure()
    
        #Создание экземпляра объекта FigureCanvas, который будет использоваться для отображения графика
        self.canvas = FigureCanvas(self.figure)
    
        #Добавление графика на макет
        self.ui.verticalLayout_17.addWidget(self.canvas)
    
        #Создание экземпляра объекта осей для графика
        self.axes = self.figure.add_subplot(projection='3d')
    
        #Вставка здесь кода для построения графика с помощью методов matplotlib
        self.axes.set_facecolor('#646464')

        self.my_cmap = plt.get_cmap("rainbow")
        self.axes.plot_trisurf(x, y, z, cmap = self.my_cmap, linewidth=0.2, edgecolors='k')
        self.axes.set_xlim(-10, 10)
        self.axes.set_ylim(-10, 10)
        self.axes.set_axis_off()
        self.axes.xaxis.pane.fill = False # Left pane
        self.axes.yaxis.pane.fill = False # Right pane
        self.figure.subplots_adjust(left=0.0, bottom=0.0, top=1.0, hspace=0.7)
        


#Создание графиков

        #График высоты
        self.Hight_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_14.addWidget(self.Hight_graph)
        self.Hight_plot = self.Hight_graph.addPlot(1, 1, 1, 1)

        self.Hight_BME_curve  = self.Hight_plot.plot(np.array([[0, 0]]))
        self.Hight_GPS_curve  = self.Hight_plot.plot(np.array([[0, 0]]))
        self.new_curve = True
        
        #print(self.Hight_BME_curve.getData())
        #print(self.Hight_GPS_curve.getData())

        self.Hight_BME_curve.setData(np.append(self.Hight_BME_curve.getData()[0], 3), np.append(self.Hight_BME_curve.getData()[1], 5))
        self.Hight_BME_curve.setPen(color='b')
        self.Hight_GPS_curve.setData(np.append(self.Hight_GPS_curve.getData()[0], 3), np.append(self.Hight_GPS_curve.getData()[1], 5))
        self.Hight_GPS_curve.setPen(color='g')

        self.legend = self.Hight_plot.addLegend()
        self.legend.addItem(self.Hight_BME_curve, 'высота по BME')
        self.legend.addItem(self.Hight_GPS_curve, 'высота по GPS')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, c")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Высота, м")
        self.Hight_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})



        #График ускорения
        self.graph1 = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_16.addWidget(self.graph1)
        self.plot1 = self.graph1.addPlot(1, 1, 1, 1)

        self.Boost_X_curve = self.plot1.plot(np.array([[0, 0]]))
        self.Boost_Y_curve = self.plot1.plot(np.array([[0, 0]]))
        self.Boost_Z_curve = self.plot1.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.Boost_X_curve.getData())
        #print(self.Boost_Y_curve.getData())
        #print(self.Boost_Z_curve.getData())

        self.Boost_X_curve.setData(np.append(self.Boost_X_curve.getData()[0], 3), np.append(self.Boost_X_curve.getData()[1], 5))
        self.Boost_X_curve.setPen(color='r')
        self.Boost_Y_curve.setData(np.append(self.Boost_Y_curve.getData()[0], 3), np.append(self.Boost_Y_curve.getData()[1], 5))
        self.Boost_Y_curve.setPen(color='g')
        self.Boost_Z_curve.setData(np.append(self.Boost_Y_curve.getData()[0], 3), np.append(self.Boost_Y_curve.getData()[1], 5))
        self.Boost_Z_curve.setPen(color='b')

        self.legend = self.plot1.addLegend()
        self.legend.addItem(self.Boost_X_curve, 'X')
        self.legend.addItem(self.Boost_Y_curve, 'Y')
        self.legend.addItem(self.Boost_Z_curve, 'Z')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, c")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Ускорение, м/с²")
        self.plot1.setAxisItems({'bottom': axis_x, 'left': axis_y})
        


        #График GPS
        self.GPS_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_10.addWidget(self.GPS_graph)
        self.GPS_plot = self.GPS_graph.addPlot(1, 1, 1, 1)

        self.GPS_curve  = self.GPS_plot.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.GPS_curve.getData())

        self.GPS_curve.setData(np.append(self.GPS_curve.getData()[0], 3), np.append(self.GPS_curve.getData()[1], 5))
        self.GPS_curve.setPen(color='#fff078')

        self.legend = self.GPS_plot.addLegend()
        self.legend.addItem(self.GPS_curve, 'координаты')
        
        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("←запад ㅤㅤㅤ м ㅤㅤㅤ восток→")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("←юг ㅤㅤㅤ м ㅤㅤㅤ север→")
        self.GPS_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})
        


        #График угловой скорости
        self.C_speed_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_15.addWidget(self.C_speed_graph)
        self.C_speed_plot = self.C_speed_graph.addPlot(1, 1, 1, 1)
        
        self.C_speed_X_curve  = self.C_speed_plot.plot(np.array([[0, 0]]))
        self.C_speed_Y_curve  = self.C_speed_plot.plot(np.array([[0, 0]]))
        self.C_speed_Z_curve  = self.C_speed_plot.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.C_speed_X_curve.getData())
        #print(self.C_speed_Y_curve.getData())
        #print(self.C_speed_Z_curve.getData())

        self.C_speed_X_curve.setData(np.append(self.C_speed_X_curve.getData()[0], 3), np.append(self.C_speed_X_curve.getData()[1], 5))
        self.C_speed_X_curve.setPen(color='r')
        self.C_speed_Y_curve.setData(np.append(self.C_speed_Y_curve.getData()[0], 3), np.append(self.C_speed_Y_curve.getData()[1], 5))
        self.C_speed_Y_curve.setPen(color='g')
        self.C_speed_Z_curve.setData(np.append(self.C_speed_Z_curve.getData()[0], 3), np.append(self.C_speed_Z_curve.getData()[1], 5))
        self.C_speed_Z_curve.setPen(color='b')

        self.legend = self.C_speed_plot.addLegend()
        self.legend.addItem(self.C_speed_X_curve, 'X')
        self.legend.addItem(self.C_speed_Y_curve, 'Y')
        self.legend.addItem(self.C_speed_Z_curve, 'Z')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, с")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Скорость, м/с")
        self.C_speed_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})
        


        #График давления
        self.Press_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_13.addWidget(self.Press_graph)
        self.Press_plot = self.Press_graph.addPlot(1, 1, 1, 1)

        self.Press_curve  = self.Press_plot.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.Press_curve.getData())

        self.Press_curve.setData(np.append(self.Press_curve.getData()[0], 3), np.append(self.Press_curve.getData()[1], 5))
        self.Press_curve.setPen(color='#fff078')

        self.legend = self.Press_plot.addLegend()
        self.legend.addItem(self.Press_curve, 'давление')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, с")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Давление, Па")
        self.Press_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})
        


        #График магнитометра
        self.Magnet_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_18.addWidget(self.Magnet_graph)
        self.Magnet_plot = self.Magnet_graph.addPlot(1, 1, 1, 1)
        
        self.Magnet_X_curve  = self.Magnet_plot.plot(np.array([[0, 0]]))
        self.Magnet_Y_curve  = self.Magnet_plot.plot(np.array([[0, 0]]))
        self.Magnet_Z_curve  = self.Magnet_plot.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.Magnet_X_curve.getData())
        #print(self.Magnet_Y_curve.getData())
        #print(self.Magnet_Z_curve.getData())

        self.Magnet_X_curve.setData(np.append(self.Magnet_X_curve.getData()[0], 3), np.append(self.Magnet_X_curve.getData()[1], 5))
        self.Magnet_X_curve.setPen(color='r')
        self.Magnet_Y_curve.setData(np.append(self.Magnet_Y_curve.getData()[0], 3), np.append(self.Magnet_Y_curve.getData()[1], 5))
        self.Magnet_Y_curve.setPen(color='g')
        self.Magnet_Z_curve.setData(np.append(self.Magnet_Z_curve.getData()[0], 3), np.append(self.Magnet_Z_curve.getData()[1], 5))
        self.Magnet_Z_curve.setPen(color='b')

        self.legend = self.Magnet_plot.addLegend()
        self.legend.addItem(self.Magnet_X_curve, 'X')
        self.legend.addItem(self.Magnet_Y_curve, 'Y')
        self.legend.addItem(self.Magnet_Z_curve, 'Z')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, с")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Сила магн. поля, Гс")
        self.Magnet_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})
        


        #График температуры
        self.Temp_graph = pg.GraphicsLayoutWidget()
        self.ui.verticalLayout_19.addWidget(self.Temp_graph)
        self.Temp_plot = self.Temp_graph.addPlot(1, 1, 1, 1)
        
        self.Temp_curve  = self.Temp_plot.plot(np.array([[0, 0]]))
        self.new_curve = True

        #print(self.Temp_curve.getData())

        self.Temp_curve.setData(np.append(self.Temp_curve.getData()[0], 3), np.append(self.Temp_curve.getData()[1], 5))
        self.Temp_curve.setPen(color='#fff078')

        self.legend = self.Temp_plot.addLegend()
        self.legend.addItem(self.Temp_curve, 'температура')

        axis_x = pg.AxisItem(orientation='bottom')
        axis_x.setLabel("Время, с")
        axis_y = pg.AxisItem(orientation='left')
        axis_y.setLabel("Температура, °С")
        self.Temp_plot.setAxisItems({'bottom': axis_x, 'left': axis_y})
#



    def makeData():
        x = np.random.rand(1000) * 20.0 - 10.0
        y = np.random.rand(len(x)) * 20.0 - 10.0

        z = np.sin(x * 0.3) * np.cos(y * 0.75)
        return x, y, z



#Обновление графиков p1 (закоментировано)   
    #def new_data_reaction_p1(self, p1):
    #    global a
    #    global arr_p1
    #    global arr_p12
    #    global arr_2
    #
    #    p1_time = p1.time / 1000.0   
    #    self.ui.label_54.setText(str(p1_time))
    #    self.ui.label_57.setText("{:.2f}".format(p1.BME280_pressure / 1000.0))
    #    self.ui.label_59.setText("{:.2f}".format(p1.BME280_temperature))
    #    self.ui.label_61.setText("{:.2f}".format(p1.height_bme))
    #    global Count1
    #    if time.time() - a < N: 
    #        arr_p1 = np.array([p1_time, p1.height_bme], [time.time(), random.uniform(1000, 2000)], [random.uniform(0, 1001), random.uniform(0, 1001)], [p1_time, p1.BME280_pressure], [p1_time, p1.BME280_temperature])
    #        print(arr_p1)  
    #        
    #    else:
    #        if (not self.new_curve_p1):
    #            add_data_to_plot(self.Hight_BME_curve, arr_p1[0], arr_p1[1])
    #            add_data_to_plot(self.Hight_GPS_curve, time.time(), random.uniform(1000, 2000))
    #            add_data_to_plot(self.GPS_curve, random.uniform(0, 1001), random.uniform(0, 1001))
    #            add_data_to_plot(self.Press_curve, arr_p1[6], arr_p1[7])
    #            add_data_to_plot(self.Temp_curve, arr_p1[8], arr_p1[9])
    #        else:
    #            self.Hight_BME_curve.setData(np.array([[arr_p1[0], arr_p1[1]]]))
    #            self.Hight_GPS_curve.setData(np.array([[time.time(), random.uniform(1000, 2000)]]))
    #            self.GPS_curve.setData(np.array([[random.uniform(0, 1001), random.uniform(0, 1001)]]))
    #            self.Press_curve.setData(np.array([[arr_p1[6], arr_p1[7]]]))
    #            self.Temp_curve.setData(np.array([[arr_p1[8], arr_p1[9]]]))
    #            self.new_curve_p1 = False
    #        a = time.time()
#
            


#Обновление графиков p1   
    def new_data_reaction_p1(self, p1):
        global dt1
        #for p1 in p1_list: p1_list[-1]:


        #p1_time = p1[-1].time  
        
        self.ui.label_57.setText("{:.2f}".format(p1[-1].BME280_pressure / 1000.0))
        self.ui.label_59.setText("{:.2f}".format(p1[-1].BME280_temperature))
        self.ui.label_61.setText("{:.2f}".format(p1[-1].height_bme))
        self.ui.label_53.setText(str(dt1))
        global Count1
        p1_time = p1[-1].time
        Hight_BME_arr = [np.array([]), np.array([])]
        Press_arr = [np.array([]), np.array([])] 
        Temp_arr = [np.array([]), np.array([])] 

        for i in range(len(p1)):
            Hight_BME_arr = [np.append(Hight_BME_arr[0], p1[i].time), np.append(Hight_BME_arr[1], p1[i].height_bme)]
            Press_arr     = [np.append(Press_arr[0], p1[i].time) , np.append(Press_arr[1], p1[i].BME280_pressure)]
        #print(Press_arr[0])
        #print(Press_arr[1])
            Temp_arr = [np.append(Temp_arr[0], p1[i].time) , np.append(Temp_arr[1], p1[i].BME280_temperature)]

        if (not self.new_curve_p1):
            add_data_to_plot(self.Hight_BME_curve, Hight_BME_arr[0], Hight_BME_arr[1], 1000)
            #add_data_to_plot(self.Hight_GPS_curve, time.time(), random.uniform(1000, 2000))
            #add_data_to_plot(self.GPS_curve, random.uniform(0, 1001), random.uniform(0, 1001))
            add_data_to_plot(self.Press_curve, Press_arr[0], Press_arr[1], 1000)
            add_data_to_plot(self.Temp_curve, Temp_arr[0], Temp_arr[1], 1000)
        else:
            self.Hight_BME_curve.setData(np.transpose(np.array(Hight_BME_arr)))
            #self.Hight_GPS_curve.setData(np.array([[time.time(), random.uniform(1000, 2000)]]))
            #self.GPS_curve.setData(np.array([[random.uniform(0, 1001), random.uniform(0, 1001)]]))
            self.Press_curve.setData(np.transpose(np.array(Press_arr)))
            self.Temp_curve.setData(np.transpose(np.array(Temp_arr)))
            self.new_curve_p1 = False
#



#Обновление состояния аппарата (p1)
        if p1[i].state == 0:
            self.ui.graphicsView_2.setStyleSheet("background-color: #fff078")
            self.ui.graphicsView_24.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_25.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_26.setStyleSheet("background-color: #646464")
            self.ui.graphicsView.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_27.setStyleSheet("background-color: #646464")
        if p1[i].state == 1:
            self.ui.graphicsView_2.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_24.setStyleSheet("background-color: #fff078")
            self.ui.graphicsView_25.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_26.setStyleSheet("background-color: #646464")
            self.ui.graphicsView.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_27.setStyleSheet("background-color: #646464")
        if p1[i].state == 2:
            self.ui.graphicsView_2.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_24.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_25.setStyleSheet("background-color: #fff078")
            self.ui.graphicsView_26.setStyleSheet("background-color: #646464")
            self.ui.graphicsView.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_27.setStyleSheet("background-color: #646464")
        if p1[i].state == 3:
            self.ui.graphicsView_2.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_24.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_25.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_26.setStyleSheet("background-color: #fff078")
            self.ui.graphicsView.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_27.setStyleSheet("background-color: #646464")
        if p1[i].state == 4:
            self.ui.graphicsView_2.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_24.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_25.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_26.setStyleSheet("background-color: #646464")
            self.ui.graphicsView.setStyleSheet("background-color: #fff078")
            self.ui.graphicsView_27.setStyleSheet("background-color: #646464")
        if p1[i].state == 5:
            self.ui.graphicsView_2.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_24.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_25.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_26.setStyleSheet("background-color: #646464")
            self.ui.graphicsView.setStyleSheet("background-color: #646464")
            self.ui.graphicsView_27.setStyleSheet("background-color: #fff078")

        Press_arr = [np.array([]), np.array([])] 
#



#Обновление графиков p12   
    def new_data_reaction_p12(self, p12):
        global dt12

        self.ui.label_48.setText("{:.2f}".format(p12[-1].latitude))
        self.ui.label_50.setText("{:.2f}".format(p12[-1].longitude))
        self.ui.label_52.setText("{:.2f}".format(p12[-1].altitude))
        self.ui.label_85.setText(str(p12[-1].fix))
        self.ui.label_86.setText(str("{:.2f}".format(p12[-1].lux)))
        self.ui.label_88.setText(str("{:.2f}".format(p12[-1].volts)))
        self.ui.label_68.setText(str(dt12))

        global Count12
        #p12_time = p12[-1].time

        GPS_arr = [np.array([]), np.array([])]
        Hight_GPS_arr = [np.array([]), np.array([])]
        for i in range(len(p12)):
            Hight_GPS_arr = [np.append(Hight_GPS_arr[0], p12[i].time), np.append(Hight_GPS_arr[1], p12[i].altitude)]
            GPS_arr     = [np.append(GPS_arr[0], p12[i].latitude) , np.append(GPS_arr[1], p12[i].longitude)]
        #print(Press_arr[0])
        #print(Press_arr[1]) 
        if (not self.new_curve_p12):
            add_data_to_plot(self.Hight_GPS_curve, Hight_GPS_arr[0], Hight_GPS_arr[1], 1000)
            add_data_to_plot(self.GPS_curve, GPS_arr[0], GPS_arr[1], 10000)
        else:
            self.Hight_GPS_curve.setData(np.transpose(np.array(Hight_GPS_arr)))
            self.GPS_curve.setData(np.transpose(np.array(GPS_arr)))
            self.new_curve_p12 = False
#



#Обновление графиков p2   
    def new_data_reaction_p2(self, p2):
        global dt2

        self.ui.label_54.setText(str("{:.2f}".format(p2[0].time)))
        self.ui.label_71.setText(str(dt2))
        #self.lib1 = ctypes.CDLL("func_de_la_function/func_de_la_function/libtest.dll")




        #global time_p2
        #global time_pr





        #time_pr = time_p2
        #time_p2 = p2.time




        #self.lib1.MadgwickAHRSupdateIMU(ctypes.pointer(p2.q), ctypes.pointer(p2.gyro_mdps[0]), ctypes.pointer(p2.gyro_mdps[1]), ctypes.pointer(p2.gyro_mdps[2]), ctypes.pointer(p2.acc_mg[0]), ctypes.pointer(p2.acc_mg[1]), ctypes.pointer(p2.acc_mg[2]), ctypes.pointer(time_p2) - time_pr, 0.3)





        global f_quat
        global Count2
        #quat = pyquaternion.Quaternion(p2.q)
        #print([float(num) for num in p2.q])

        #f_quat.writelines([str(num) for num in p2.q])
        #f_quat.write('hi')
        #f_quat.write('/n')

        #print("and here")

        Boost_X_arr = [np.array([]), np.array([])]
        Boost_Y_arr = [np.array([]), np.array([])]
        Boost_Z_arr = [np.array([]), np.array([])]
        C_speed_X_arr = [np.array([]), np.array([])]
        C_speed_Y_arr = [np.array([]), np.array([])]
        C_speed_Z_arr = [np.array([]), np.array([])]
        Magnet_X_arr = [np.array([]), np.array([])]
        Magnet_Y_arr = [np.array([]), np.array([])]
        Magnet_Z_arr = [np.array([]), np.array([])] 
        for i in range(len(p2)):
            #Hight_BME_arr = np.append(Hight_BME_arr, [p1[i].time, p1[i].height_bme])
            Boost_X_arr = [np.append(Boost_X_arr[0], p2[i].time) , np.append(Boost_X_arr[1], p2[i].acc_mg[0])]
            Boost_Y_arr = [np.append(Boost_Y_arr[0], p2[i].time) , np.append(Boost_Y_arr[1], p2[i].acc_mg[1])]
            Boost_Z_arr = [np.append(Boost_Z_arr[0], p2[i].time) , np.append(Boost_Z_arr[1], p2[i].acc_mg[2])]
            C_speed_X_arr = [np.append(C_speed_X_arr[0], p2[i].time) , np.append(C_speed_X_arr[1], p2[i].gyro_mdps[0])]
            C_speed_Y_arr = [np.append(C_speed_Y_arr[0], p2[i].time) , np.append(C_speed_Y_arr[1], p2[i].gyro_mdps[1])]
            C_speed_Z_arr = [np.append(C_speed_Z_arr[0], p2[i].time) , np.append(C_speed_Z_arr[1], p2[i].gyro_mdps[2])]
            Magnet_X_arr = [np.append(Magnet_X_arr[0], p2[i].time) , np.append(Magnet_X_arr[1], p2[i].LIS3MDL_magnetometer[0])]
            Magnet_Y_arr = [np.append(Magnet_Y_arr[0], p2[i].time) , np.append(Magnet_Y_arr[1], p2[i].LIS3MDL_magnetometer[1])]
            Magnet_Z_arr = [np.append(Magnet_Z_arr[0], p2[i].time) , np.append(Magnet_Z_arr[1], p2[i].LIS3MDL_magnetometer[2])]
        #print(Press_arr[0])
        #print(Press_arr[1])
        self.Orient._update_rotation([float(num) for num in p2[-1].q])
        #p2_time = p2.time
        self.ui.label_12.setText("{:.2f}".format(p2[-1].gyro_mdps[0]))
        self.ui.label_14.setText("{:.2f}".format(p2[-1].gyro_mdps[1]))
        self.ui.label_16.setText("{:.2f}".format(p2[-1].gyro_mdps[2]))
        self.ui.label_18.setText("{:.2f}".format(sqrt(p2[-1].gyro_mdps[0]*p2[-1].gyro_mdps[0]+p2[-1].gyro_mdps[1]*p2[-1].gyro_mdps[1]+p2[-1].gyro_mdps[2]*p2[-1].gyro_mdps[2])))
        self.ui.label_21.setText("{:.2f}".format(p2[-1].q[0]))
        self.ui.label_23.setText("{:.2f}".format(p2[-1].q[1]))
        self.ui.label_25.setText("{:.2f}".format(p2[-1].q[2]))
        self.ui.label_27.setText("{:.2f}".format(p2[-1].q[3]))
        self.ui.label_63.setText("{:.2f}".format(p2[-1].lidar))
        self.ui.label_6.setText("{:.2f}".format(p2[-1].acc_mg[0]))
        self.ui.label_7.setText("{:.2f}".format(p2[-1].acc_mg[1]))
        self.ui.label_8.setText("{:.2f}".format(p2[-1].acc_mg[2]))
        self.ui.label_9.setText("{:.2f}".format(sqrt(p2[-1].acc_mg[0]*p2[-1].acc_mg[0]+p2[-1].acc_mg[1]*p2[-1].acc_mg[1]+p2[-1].acc_mg[2]*p2[-1].acc_mg[2])))
        self.ui.label_30.setText("{:.2f}".format(p2[-1].LIS3MDL_magnetometer[0]))
        self.ui.label_32.setText("{:.2f}".format(p2[-1].LIS3MDL_magnetometer[1]))
        self.ui.label_34.setText("{:.2f}".format(p2[-1].LIS3MDL_magnetometer[2]))
        self.ui.label_36.setText("{:.2f}".format(sqrt(p2[-1].LIS3MDL_magnetometer[0]*p2[-1].LIS3MDL_magnetometer[0]+p2[-1].LIS3MDL_magnetometer[1]*p2[-1].LIS3MDL_magnetometer[1]+p2[-1].LIS3MDL_magnetometer[2]*p2[-1].LIS3MDL_magnetometer[2])))
        if (not self.new_curve_p2):
            imu_limit = 500
            add_data_to_plot(self.Boost_X_curve, Boost_X_arr[0], Boost_X_arr[1], imu_limit)
            add_data_to_plot(self.Boost_Y_curve, Boost_X_arr[0], Boost_Y_arr[1], imu_limit)
            add_data_to_plot(self.Boost_Z_curve, Boost_X_arr[0], Boost_Z_arr[1], imu_limit)
            add_data_to_plot(self.C_speed_X_curve, C_speed_X_arr[0], C_speed_X_arr[1], imu_limit)
            add_data_to_plot(self.C_speed_Y_curve, C_speed_Y_arr[0], C_speed_Y_arr[1], imu_limit)
            add_data_to_plot(self.C_speed_Z_curve, C_speed_Z_arr[0], C_speed_Z_arr[1], imu_limit)
            add_data_to_plot(self.Magnet_X_curve, Magnet_X_arr[0], Magnet_X_arr[1], imu_limit)
            add_data_to_plot(self.Magnet_Y_curve, Magnet_Y_arr[0], Magnet_Y_arr[1], imu_limit)
            add_data_to_plot(self.Magnet_Z_curve, Magnet_Z_arr[0], Magnet_Z_arr[1], imu_limit)
        else:
            self.Boost_X_curve.setData(np.transpose(np.array(Boost_X_arr)))
            self.Boost_Y_curve.setData(np.transpose(np.array(Boost_Y_arr)))
            self.Boost_Z_curve.setData(np.transpose(np.array(Boost_Z_arr)))
            self.C_speed_X_curve.setData(np.transpose(np.array(C_speed_X_arr)))
            self.C_speed_Y_curve.setData(np.transpose(np.array(C_speed_Y_arr)))
            self.C_speed_Z_curve.setData(np.transpose(np.array(C_speed_Z_arr)))
            self.Magnet_X_curve.setData(np.transpose(np.array(Magnet_X_arr)))
            self.Magnet_Y_curve.setData(np.transpose(np.array(Magnet_Y_arr)))
            self.Magnet_Z_curve.setData(np.transpose(np.array(Magnet_Z_arr)))
            self.new_curve_p2 = False
#



        
    def closeEvent(self, evnt):
        self.data_object.finish()
        start_time = time.time()
        while self.data_thread.isRunning():
            if (time.time() - start_time) > 2:
                break
            time.sleep(0.01)
        super(App, self).closeEvent(evnt)
#




if __name__ == "__main__":


    QtCore.QCoreApplication.setOrganizationName("CNIImash")
    QtCore.QCoreApplication.setApplicationName("Neon_Blade")

    application = QApplication(argv)
    window = App()
    window.show()
    exit(application.exec_())
    application.exit()
    f = f_quat.read()
    print(f)
    #f_quat.close()
    file_acc.close()
    file_mag.close()
