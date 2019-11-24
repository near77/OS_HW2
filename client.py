import numpy as np
import cv2
import socket
import sys

if len(sys.argv)<4:
    print('usage : [ ip ] [ port ] [ file name ]')
    sys.exit()

ip=sys.argv[1]
port=int(sys.argv[2])
sock=socket.socket()
sock.connect((ip,port))

name=sys.argv[3]
sock.send(name.encode('utf-8'))

frame = cv2.imread("./LicPlateImages/1.png")
_,imgencode=cv2.imencode('.jpg',frame,[int(cv2.IMWRITE_JPEG_QUALITY),90])
data=np.array(imgencode)
strdata=data.tostring()
sock.send(str(len(strdata)).ljust(16).encode('utf-8'))
sock.send(strdata)


