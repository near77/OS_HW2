import socket
import numpy as np
import cv2

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7070        # The port used by the server

image = cv2.imread("plates/1.png")
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
_, img_encode = cv2.imencode(".jpeg", image, encode_param)
data = np.array(img_encode)
stringData = data.tostring()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    file_name = "../01.mp4"
    s.send(file_name.encode())
    s.send(str(len(stringData)).ljust(16).encode())
    s.send(stringData)
    s.close()