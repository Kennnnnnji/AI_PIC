import imtrans
import os
import cv2
import sys

video_addr = sys.argv[1]
modelNumber = int(sys.argv[2])
outputFolderPath = sys.argv[3]
modelPath = imtrans.model_addr[modelNumber]
(videoPath,videoFullName) = os.path.split(video_addr)
videoName = os.path.splitext(videoFullName)[0]
suffixName = os.path.splitext(videoFullName)[-1].lower()

mp3Path = imtrans.getVideoMp3(video_addr)
video = imtrans.makeVideoCapture(video_addr)

fourcc = cv2.VideoWriter_fourcc(*imtrans.decoder_list[suffixName])
outputMPath = outputFolderPath + videoName + "-output" + suffixName
out = cv2.VideoWriter(outputMPath, fourcc, video.getFps(), video.getSize())

dnn = cv2.dnn.readNetFromTorch(modelPath)

#important: totalFrames is a float object
for i in range(int(video.getTotalFrames())):
    out.write(imtrans.dnnFrameProcess(video.getFrameList()[i], dnn))
    print(i)

out.release()
imtrans.videoAddMp3(outputMPath, mp3Path)
