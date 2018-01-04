import picamera
import time

cam=picamera.PiCamera()
cam.start_preview()
time.sleep(20)
cam.stop_preview()

#cam.start_recording('/home/guy/video.h264')
#time.sleep(5)
#cam.stop_recording()
