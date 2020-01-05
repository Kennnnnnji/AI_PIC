# author:    tq,junxiong,yuma
# version = 1.0

# import the necessary packages
import cv2
import numpy
import subprocess
import time
import os

class Video:
    def __init__(self, videoCapture, fps, size, totalFrames):
        self.__fps = fps
        self.__size = size
        self.__totalFrames = totalFrames
        self.__frameList = []
        success, image = videoCapture.read()
        while success:
            self.__frameList.append(image)
            success, image = videoCapture.read()
    def getFps(self):
        return self.__fps
    def getSize(self):
        return self.__size
    def getTotalFrames(self):
        return self.__totalFrames
    def getFrameList(self):
        return self.__frameList

def getVideoMp3(videoPath):
    mp3Path = videoPath.split('.')[0] + str(time.time_ns()) + '.mp3'
    cmd = 'ffmpeg -i ' + videoPath + ' -f mp3 ' + mp3Path
    subprocess.call(cmd, shell=True)
    return mp3Path

def videoAddMp3(videoPath, mp3Path):
    suffixName = videoPath.split('.')[-1].lower()
    outputPath = videoPath.split('.')[0] + '-' + str(time.time_ns()) + '.' + suffixName
    cmd = 'ffmpeg -i ' + videoPath + ' -i ' + mp3Path + ' -strict -2 -f ' + suffixName + ' ' + outputPath
    subprocess.call(cmd, shell = True)

    os.remove(videoPath)
    os.remove(mp3Path)
    #subprocess.call('del ' + videoPath, shell=True)
    #subprocess.call('del ' + mp3Path, shell=True)
    return outputPath

def imageResize(image, width):
    r = float(width) / image.shape[1]
    dim = (width, int(image.shape[0] * r))
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image

def dnnFrameProcess(image, dnn, mode=2):
    '''
    eturn type of data
    0 is float in (0,1)
    1 is float in (0,255)
    2 is uint8 in (0,255)
    '''

    (origin_h, origin_w) = image.shape[:2]

    image = imageResize(image, width=600)
    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
                                 (103.939, 116.779, 123.680), swapRB=False, crop=False)
    dnn.setInput(blob)
    output = dnn.forward()
    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 101.696
    output[1] += 108.156
    output[2] += 115.926
    output = output.transpose(1, 2, 0)

    # make the output size same with input size
    output = imageResize(output, origin_w)

    # march the mode
    if mode == 0:
        output /= 255
    elif mode == 1:
        output = output
    elif mode == 2:
        output = numpy.uint8(output)

    return output

def dnnFrameProcessGpu(image, dnn, mode=2):
    '''
    eturn type of data
    0 is float in (0,1)
    1 is float in (0,255)
    2 is uint8 in (0,255)
    '''

    (origin_h, origin_w) = image.shape[:2]

    image = imageResize(image, width=600)
    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
                                 (103.939, 116.779, 123.680), swapRB=False, crop=False)
    dnn.setInput(blob)
    output = dnn.forward()
    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 101.696
    output[1] += 108.156
    output[2] += 115.926
    output = output.transpose(1, 2, 0)

    # make the output size same with input size
    output = imageResize(output, origin_w)

    # march the mode
    if mode == 0:
        output /= 255
    elif mode == 1:
        output = output
    elif mode == 2:
        output = numpy.uint8(output)

    return output

def makeVideoCapture(videoPath):
    videoCapture = cv2.VideoCapture(videoPath)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    totalFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    video = Video(videoCapture,fps,size,totalFrames)
    return video


model_addr = (
    'models\\eccv16\\composition_vii.t7',
    "models\\eccv16\\la_muse.t7",
    'models\\eccv16\\starry_night.t7',
    'models\\eccv16\\the_wave.t7',
    'models\\instance_norm\\candy.t7',
    'models\\instance_norm\\feathers.t7',
    'models\\instance_norm\\la_muse.t7',
    'models\\instance_norm\\mosaic.t7',
    'models\\instance_norm\\starry_night.t7',
    'models\\instance_norm\\the_scream.t7',
    'models\\instance_norm\\udnie.t7'
)

decoder_list = {
    '.mp4': 'mp4v',
    '.avi': 'H264',
    '.flv': 'flv1'
}
