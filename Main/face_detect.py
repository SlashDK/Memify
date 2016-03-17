import cv2
import sys
import datetime
import numpy

def addItems(frame,faces,mouths,eyes):
    glasses = cv2.imread("glasses.png",-1)
    joint = cv2.imread("joint.png",-1)
    
    t=datetime.datetime.now().time()
    filename="Saved/"+str(t.hour)+str(t.minute)+str(t.second)+".jpg"
    #print(frame[0,0])
    #print(joint)
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in eyes:
            if(x2>x and x2+w2<x+w and y2>y and y2+h2<y+h):
                glasses=cv2.resize(glasses,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] =  glasses[:,:,c] * (glasses[:,:,3]/255.0) + frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] * (1.0 - glasses[:,:,3]/255.0)
        for (x2, y2, w2, h2) in mouths:
            if(x2>x and x2<x+w):
                joint=cv2.resize(joint,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/5:y2+6*h2/5, x2+w2/2:x2+3*w2/2, c] =  joint[:,:,c] * (joint[:,:,3]/255.0) + frame[y2+h2/5:y2+6*h2/5, x2+w2/2:x2+3*w2/2, c] * (1.0 - joint[:,:,3]/255.0)


    cv2.imwrite(filename,frame)
    return 

#realpython.com
def capVideo():
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    mouthCascade = cv2.CascadeClassifier("Mouth.xml")
    eyesCascade = cv2.CascadeClassifier("frontalEyes35x16.xml")
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        ret, orig = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        mouths = mouthCascade.detectMultiScale(
            gray,
            scaleFactor=1.7,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        eyes = eyesCascade.detectMultiScale(
            gray,
            scaleFactor=1.01,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        for (x, y, w, h) in mouths:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 1)
        
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        
        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            #orig=cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
            addItems(orig,faces,mouths,eyes)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

capVideo()

