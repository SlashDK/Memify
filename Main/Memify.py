import cv2
import sys
import datetime
import numpy
import subprocess

def makeThug(frame,faces,mouths,eyes):
    glasses = cv2.imread("glasses.png",-1)
    joint = cv2.imread("joint.png",-1)
    t=datetime.datetime.now().time()
    filename="Saved/"+str(t.hour)+str(t.minute)+str(t.second)+".jpg"
    #work only inside faces
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in eyes:
            if(x2>x and x2+w2<x+w and y2>y and y2+h2<y+h and y2+h2/2<y+h/2 and x2+w2/2>x+h/3 and x2+w2/2<x+2*h/3):
                glasses=cv2.resize(glasses,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] =  glasses[:,:,c] * (glasses[:,:,3]/255.0) + frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] * (1.0 - glasses[:,:,3]/255.0)
                break
        for (x2, y2, w2, h2) in mouths:
            if(x2>x and x2<x+w and y2>y+h/2 and y2+h2<y+5*h/4 and x2+w2/2>x+h/3 and x2+w2/2<x+2*h/3):
                joint=cv2.resize(joint,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/4:y2+5*h2/4, x2+w2/2:x2+3*w2/2, c] =  joint[:,:,c] * (joint[:,:,3]/255.0) + frame[y2+h2/4:y2+5*h2/4, x2+w2/2:x2+3*w2/2, c] * (1.0 - joint[:,:,3]/255.0)
                break

    cv2.imwrite(filename,frame)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def makeVideo(frame,w,h,mkey):
    fps=25
    capSize = (int(w),int(h))
    fourcc=cv2.cv.CV_FOURCC('m','p','4','v')
    out = cv2.VideoWriter() 
    success = out.open('output.mov',fourcc,fps,capSize,True) 
    frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    # for i in range(100):
    #     temp=cv2.resize(frame,(int(w)+int(w*i/100),int(h)+int(h*i/100)))
    #     #tempFrame = temp[i/2:int(h)+i/2,i/2:int(w)+i/2]
    #     tempFrame = temp[int((h+h*i/100)/2 - h/2):int((h+h*i/100)/2 + h/2) + 10,
    #     int((w+w*w/100)/2 - w/2):int((w+w*i/100)/2 + w/2) +10]
    #     tempFrame=tempFrame[0:int(h),0:int(w)]
    #     out.write(tempFrame)
    # for i in range (65):
    #     out.write(tempFrame)
    if mkey == 'p':
        for i in range(162):
            temp=cv2.resize(frame,(int(w)+2*i,int(h)+2*i))
            tempFrame = temp[i/2:int(h)+i/2,i/2:int(w)+i/2]
            out.write(tempFrame)
        out.release() 
        out=None
        #add audio and make final video
        cmd = 'ffmpeg -y -i Final.mp4 -r 30 -i output.mov -filter:a aresample=async=1 -c:a flac -c:v copy -shortest result.mkv'
        subprocess.call(cmd, shell=True)                                     # "Muxing Done
        print('Muxing Done')
        cmd = '~/../../Applications/VLC.app/Contents/MacOS/VLC "result.mkv" -f --play-and-stop'
        subprocess.call(cmd, shell=True) 

#realpython.com
def capVideo():
    #initialize cascades
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    mouthCascade = cv2.CascadeClassifier("Mouth.xml")
    eyesCascade = cv2.CascadeClassifier("frontalEyes35x16.xml")
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # save for later use
        ret, orig = video_capture.read()
        # for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
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
            scaleFactor=1.1,
            minNeighbors=10,
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
            w,h=video_capture.get(3),video_capture.get(4)
            finalImage=makeThug(orig,faces,mouths,eyes)
            makeVideo(finalImage,w,h,'p')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

capVideo()

