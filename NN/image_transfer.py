import cv2
import time
import imtrans
import sys

imageAddr = sys.argv[1]
modelId = int(sys.argv[2])
outputAddr = sys.argv[3]

modelAddr = modelPath = imtrans.model_addr[modelId]

dnn = cv2.dnn.readNetFromTorch(modelPath)

image = cv2.imread(imageAddr)
output = imtrans.dnnFrameProcess(image, dnn)

cv2.imwrite(outputAddr,output)
