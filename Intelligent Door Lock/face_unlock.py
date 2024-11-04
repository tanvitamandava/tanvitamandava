#!/usr/bin/python

import RPi.GPIO as GPIO
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

# Initialize GPIO
GPIO_PIN = 4
GPIO_LED_GREEN = 17
GPIO_LED_RED = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)
GPIO.setup(GPIO_LED_GREEN, GPIO.OUT)
GPIO.setup(GPIO_LED_RED, GPIO.OUT)

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# Load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

vs = VideoStream(src=0).start()
time.sleep(2.0)

# Start the FPS counter
fps = FPS().start()

# Flag to indicate if the green LED has blinked for "shreyas" detection
green_led_blinked = False

# Flag to indicate if GPIO pin was set high due to no face
no_face_high_set = False

# Loop over frames from the video file stream
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    if len(boxes) == 0:
        if not no_face_high_set:
            GPIO.output(GPIO_PIN, GPIO.HIGH)  # Set GPIO high when no face is detected
            no_face_high_set = True
        green_led_blinked = False
        GPIO.output(GPIO_LED_RED, GPIO.LOW)  # Turn off red LED when no face is detected
    else:
        no_face_high_set = False
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)

                if name == "shreyas":
                    GPIO.output(GPIO_PIN, GPIO.LOW)  # Set GPIO low when "shreyas" is detected
                    if not green_led_blinked:
                        GPIO.output(GPIO_LED_GREEN, GPIO.HIGH)
                        time.sleep(0.5)
                        GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
                        green_led_blinked = True
                else:
                    GPIO.output(GPIO_PIN, GPIO.HIGH)  # Set GPIO high for others
                    GPIO.output(GPIO_LED_RED, GPIO.HIGH)  # Turn on red LED when face is detected but not "shreyas"
            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
GPIO.cleanup()