from flask import Flask, request
from flask_cors import CORS
import json
from detect import run as camera
import requests
import cv2
import json

app = Flask(__name__)
CORS(app)


class Value:
    value = {}


value = Value()
@app.route("/info", methods=["GET"])
def handle_request():
    print(value.value)
    return json.dumps(value.value)


@app.route("/info", methods=["POST"])
def handle_post():
    req = json.loads(request.data)
    res = {"status": "OK"}
    value.value = req

    return json.dumps(res)


@app.route("/start", methods=["POST"])
def handle_start():
    res = {"status": "OK"}
    camera()
    return json.dumps(res)


@app.route("/start2", methods=["POST"])
def handle_start2():
    res = {"status": "OK"}
    face_cascade = cv2.CascadeClassifier(
        'D:/JOAQUIN/Tiquero/Software/Desktop/Squats/python/haarcascade_frontalface_default.xml')

    # To capture video from webcam.
    cap = cv2.VideoCapture(0)
    # To use a video file as input
    # cap = cv2.VideoCapture('filename.mp4')
    lastStates = []
    thres = 7
    counter = 0
    state = False
    didSquat = True
    serv = True
    status = ""
    sets = 0
    setGoal = 30
    while True:
        # Read the frame
        _, img = cap.read()

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        altura = int((len(gray)/2))
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # asks if face is below line
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            if y+h > altura:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                state = True

            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                state = False

        cv2.line(img, (0, altura), (len(gray[0])-1, altura),
                 color=[255, 255, 255], thickness=1)
        # process and checks if user made a squat
        lastStates.append(state)
        if len(lastStates) >= thres:
            lastStates.pop(0)

        if all(lastStates) and not didSquat:
            counter += 1
            print(counter)
            didSquat = True
            status = "DOWN"

        if not any(lastStates):
            didSquat = False
            status = "UP"

        # cv2.putText(img, "count: " + str(counter), (400, 400),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, thickness=3, color=[255, 255, 255])
        # cv2.putText(img, "status: " + str(status), (400, 440),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, thickness=3, color=[255, 255, 255])
        value.value = {"counter": str(
            counter), "status": status, "set": setGoal, "image": img.tolist()}
        # Display
        if counter == setGoal:
            counter = 0
            sets += 1
            setGoal -= 1
        if setGoal == 0:
            setGoal = "success!"
        cv2.imshow('img', img)

        # Stop if escape key is pressed
        k = cv2.waitKey(32)

        if k == 32:
            counter = 0

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    # Release the VideoCapture object
    cap.release()

    return json.dumps(res)


app.run()
