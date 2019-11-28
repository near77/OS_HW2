import os
import cv2
import time
import socket
import threading
import numpy as np
from Extraction import LicencePlateDetector

HOST = "127.0.0.1"
PORT = 7070

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def DataProcessor(filename, frame_array):
    """
    Write per frame or Record all frames then write
    """
    filename = filename.split(".")[-2]+"tmp"
    
    while os.path.exists(filename):
        tmp_int = 0
        filename = filename + str(tmp_int)
        tmp_int += 1

    f = open(filename+".txt", "w")
    f.close()
    f = open(filename+".txt", "a")
    for frame in frame_array:
        f.write(str(frame)+'\n')
    f.close()

def FileReceiver(conn, filename):
    frame_count = 1
    frame_array = []
    while True:
        stime = time.time()
        length = conn.recv(16)
        if not length:
            break
        # print("Image size: ", length)
        stringData = recvall(conn, int(length))
        if not stringData:
            break
        data = np.fromstring(stringData, dtype="uint8")
        decimg = cv2.imdecode(data, 1)
        have_lic = LicencePlateDetector(decimg)
        # have_lic = True
        if(have_lic):
            frame_array.append(frame_count)
            print("Licence Plate Detected.")
        else:
            print("There is no Licence Plate.")
        print("Time per frame: ", time.time() - stime)
        frame_count += 1
    DataProcessor(filename, frame_array)
        

def main():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                file_name = conn.recv(9)
                print("File name: ",file_name.decode())
                FileReceiver(conn, file_name.decode())
            

if __name__ == "__main__":
    main()    