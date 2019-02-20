# USAGE
# python shallownet_load.py --dataset ../datasets/animals --model shallownet_weights.hdf5
# bluetooth functionality added
# import the necessary packages
# switch functionality added
#1.4 added load_cell functionality

from pyimagesearch.preprocessing import ImageToArrayPreprocessor
from pyimagesearch.preprocessing import SimplePreprocessor
from pyimagesearch.datasets import SimpleDatasetLoader2
from keras.models import load_model
from imutils import paths
import numpy as np
import argparse
import cv2
import operator
import serial,time
import load_cell
import RPi.GPIO as gpio
sw = 7
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(sw,gpio.IN)

# initialize the class labels
classLabels = ["beans","brinjal","chilli","tomato"]

#initialise the serial port
port = serial.Serial("/dev/ttyUSB1",baudrate=9600, timeout=1)

# initialize the image preprocessors

sp = SimplePreprocessor(100, 100)
iap = ImageToArrayPreprocessor()

# load the pre-trained network
print("[INFO] loading pre-trained network...")
port.write(bytes(("loading pre-trained network..."+"\r\n"),'UTF-8'))
model = load_model("veges.hdf5")


# loop over the sample images
while True:
        inp = gpio.input(sw)
        print("waiting for switch press")
        if(inp ==1):
                print("switch pressed")
                cap = cv2.VideoCapture(0)
                #variable to hold the variable of the prediction
                avg = 0
                i=0
                while(i<5):
                        ret,frame = cap.read()

                        # load the dataset from disk then scale the raw pixel intensities to the range [0, 1]
                        sdl = SimpleDatasetLoader2(preprocessors=[sp, iap])
                        (data) = sdl.load(frame)
                        data = data.astype("float") / 255.0

                        

                        # make predictions on the images
                        #print("[INFO] predicting...")
                        preds = model.predict(data)[0]
                        index, value = max(enumerate(preds), key=operator.itemgetter(1))
                        print("index",index)
                        #cv2.putText(frame, "Label: {}".format(classLabels[index]),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        #port.write(bytes(("{}".format(classLabels[index])+"\r\n"),'UTF-8'))
                        cv2.imshow("Image", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                cap.release()
                                cv2.destroyAllWindows()	
                                break
                        i+=1
                        avg = avg + index
                cap.release()
                cv2.destroyAllWindows()
                if(i==5):
                        wei = load_cell.weight()
                        mass = 8423200 - wei
                        j=int(avg/5)
                        print("{}".format(classLabels[int(avg/5)]))
                        port.write(bytes(("item={}  weight={}".format(classLabels[j],int(mass/425))+"\r\n"),'UTF-8'))
                        
