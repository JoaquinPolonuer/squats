import requests
import cv2
import json
# Load the cascade

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

    cv2.putText(img, "count: " + str(counter), (400, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1, thickness=3, color=[255, 255, 255])
    cv2.putText(img, "status: " + str(status), (400, 440),
                cv2.FONT_HERSHEY_SIMPLEX, 1, thickness=3, color=[255, 255, 255])
    if serv:
        try:
            r = requests.post("http://127.0.0.1:5000/info",
                              data=json.dumps({"counter": str(counter), "status": status}))
        except:
            serv = False
            pass
    # Display
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
