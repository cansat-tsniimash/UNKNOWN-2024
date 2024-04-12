from picamera2 import Picamera2
picam2 = Picamera2()
picam2.start_and_record_video(output="/home/knpn/cam/test.mp4", duration=10)
