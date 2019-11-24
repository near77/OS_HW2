import os
import io
import cv2
import sys
import socket
import threading
import numpy as np
from _thread import *

import packages.DetectChars
import packages.DetectPlates
import packages.PossiblePlate

MAX_CLIENT = 25
num_of_client = 0

num_of_client_lock = threading.Lock()

def Data_Processor():
    pass

def Licence_Plate_Detector():
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return                                                          # and exit program
    # end if
    imgOriginalScene  = cv2.imread("LicPlateImages/1.png")               # open image

    if imgOriginalScene is None:                            # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:                                                       # else
                # if we get in here list of possible plates has at leat one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return                                          # and exit program
        # end if
        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")


def File_Receiver(conn):
    global num_of_client
    file_name = conn.recv(20).decode()
    print("File name: ", file_name)
    file_length = int(conn.recv(10).decode())
    print("File Length: ", file_length)
    file_content = conn.recv(file_length)
    print(file_content)
    file_content = np.frombuffer(file_content, dtype="uint8")
    print(file_content)
    file_content = cv2.imdecode(file_content, 1)
    print(file_content)
    # cv2.imshow("img", file_content)
    # cv2.waitKey(0)

    conn.close()

    num_of_client_lock.acquire()
    num_of_client += 1
    num_of_client_lock.release()
    

def main():
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    global num_of_client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Socket is listening...")
        while True:
            while num_of_client >= MAX_CLIENT:
                pass
            conn, addr = s.accept()

            num_of_client
            num_of_client_lock.acquire()
            num_of_client += 1
            num_of_client_lock.release()

            start_new_thread(File_Receiver, (conn, ))
        s.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing HOST or PORT info.")
    else:
        #print("Woala")
        main()