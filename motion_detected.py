import argparse
import time
import cv2
import datetime
import numpy as np

#현재 설정
#fps=15, video size = 640*480
#3 frame 당 한번씩 motion detect
#터미널 혹은 cmd에서 python -m 파이썬코드.py -v 동영상이름 으로 하면 저장된 동영상에 대해서 motion detect 수행
#ex. python -m test.py -a 8000 
#검출 모션 픽셀 크기가 최소 8000
#ps. 파이썬에서 경로 설정 시 \ 대신 /로 설정

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the vidio file")
ap.add_argument("-a","--min-area", type=int, default=500, help="minimum area size")
args =  vars(ap.parse_args())

# count frame number
count = 0
 
# save video --> not completed
#fourcc = cv.VideoWriter_fourcc('M','J','P','G')
#out = cv.VideoWriter("C:/Python27/test_image/out.avi",fourcc, 20.0,(640,480))

#if the video argument is None, then we are reading from pibcam
if args.get("video",None) is None:
    camera = cv2.VideoCapture(0)
    print("No camera")
    time.sleep(0.25)
    #video fps setting
    camera.set(cv2.CAP_PROP_FPS, 15)
#otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])

#initialize the first frame in the video stream
firstFrame = None

#loop over the frames of the video
while True:
    count = count+1
    #grab the current frame and initialize the occupied/unoccupied
    #text
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
    #if the frame could not be grabbed,
    #  then we have reached the end of the video
    if not grabbed:
        break

    #resize the frame, covert it to grayscale, and blur it
    frame = cv2.resize(frame, (640,480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    #fps 출력
    fps = camera.get(cv2.CAP_PROP_FPS)
    print(fps)
    #if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    #compute the absolute difference between the current frame and
    #first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    #dilate the thresholded image to fill in holes, then find contours
    #on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)

    ###Value Error: not enough values to unpack(expected 3, got 2)
    ###python version2 code like: (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ###python version3 code like: (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #loop over the contours count region in each frame
    count2 = 0
    if(count % 10 ==0):
        for c in cnts:
            count2 = count2 + 1
            #if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            #compute the bounding box for the contour, draw it on the frame, 
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #save update the text
            img_trim = frame[y:y+h, x:x+w]
            #raspberry 실행시 motion_detect image save경로 재설정 필수
            cv2.imwrite("D:/VMD_test_image/frame%d_%d.jpg"%(count, count2), img_trim)
            text = "Occupied"
    #draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #show the frame and recod if the user presses a key
    cv2.imshow("Security Feed", frame)
    #out.wirte(frame)
    cv2.imshow("Trash", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    #if the 'q' key is pressed, break from the lop
    if key ==ord("q"):
        break
# cleanup the camera and close any open windows
camera.release()
#out.release()
cv2.destroyAllWindows()