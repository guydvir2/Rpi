import picamera
import time

camera = picamera.PiCamera()
#camera.resolution = (1920, 1080)
#
camera.resolution = (1024, 768)

# camera.capture('/home/guy/image.jpg')
#camera.brightness = 70 # 0 - 100
camera.start_preview()
#for i in range(100):
    #camera.brightness = i
    #time.sleep(0.2)
    
time.sleep(15)
camera.stop_preview()

camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
