
import numpy as np
import urllib
import cv2
 
img = cv2.imread('./LicPlateImages/1.png')
# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
img_encode = cv2.imencode('.jpg', img)[1]
# imgg = cv2.imencode('.png', img)
 
data_encode = np.array(img_encode)
str_encode = data_encode.tostring()

# # 缓存数据保存到本地，以txt格式保存
# with open('img_encode.txt', 'wb') as f:
#     f.write(str_encode)
#     f.flush
 
# with open('img_encode.txt', 'rb') as f:
#     str_encode = f.read()
 
image = np.asarray(bytearray(str_encode), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imshow('img_decode',image)
cv2.waitKey()