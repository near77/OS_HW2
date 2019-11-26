import socket
import numpy as np
import cv2
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

def FileReceiver(conn):
    """
    input: int length --> Received image size
    Purpose: 
    """
    while True:
        length = conn.recv(16)
        if not length:
            break
        print("Image size: ", length)
        stringData = recvall(conn, int(length))
        if not stringData:
            break
        data = np.fromstring(stringData, dtype="uint8")
        decimg = cv2.imdecode(data, 1)
        have_lic = LicencePlateDetector(decimg)

        if(have_lic):
            print("Licence Plate Detected.")
        else:
            print("There is no Licence Plate.")

def main():
    while(True):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                file_name = conn.recv(9)
                print("File name: ",file_name)
                FileReceiver(conn)
            

if __name__ == "__main__":
    main()    