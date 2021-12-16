import cv2
import numpy as np
import argparse
import time
import datetime
a, b, c = None, None, None

#argument parser 구성 및 분석
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

#video argument is None --> find conected cam
if args.get("video",None) is None:
    camera = cv2.VideoCapture(0)
    print("Camera conected!!")
    time.sleep(0.25)
    #video fps stting --> 적용 안되는거같음 찾아봐야함
    camera.set(cv2.CAP_PROP_FPS, 20)
else:
    #otherwise, reading from video file
    print("Camera disconected!!")
    camera = cv2.VideoCapture(args["video"]) 
 
if camera.isOpened():
    ret, a = camera.read()
    ret, b = camera.read()
    count = 0
    while ret:   
        fps = camera.get(cv2.CAP_PROP_FPS)     
        print(fps)
        count = count + 1 
        ret, c = camera.read()
        draw = c.copy()      
        if not ret:
            break
        #연산속도를 높이기 위해 그레이스케일링 영상으로 변환
        a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)

        #a, b, c를 비교
        diff1 = cv2.absdiff(a_gray, b_gray)        
        diff2 = cv2.absdiff(b_gray, c_gray)

        #차이가 25 이상이면 255(흰색), 작으면 0(검정색)
        ret, diff1_t = cv2.threshold(diff1, 25, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, 25, 255, cv2.THRESH_BINARY)
 
        #cv2.bitwiase_and를 이용하여 a, b, c 간의 차이 비교
        diff = cv2.bitwise_and(diff1_t, diff2_t)

        #모노폴로지 연산을 위한 구조요소 생성
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        #모노폴로지 연산을 통해 노이즈 제거 및 선명도 상승
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel) 
        diff_cnt = cv2.countNonZero(diff)
        count2 = 0

        if diff_cnt > 5:
            count2 = count2 + 1   
            #nzero: diff는 카메라 영상과 사이즈가 같으며, a, b프레임의 차이 어레이를 의미함. 즉 0이 아닌 index을 return
            nzero = np.nonzero(diff)
            #(min(nzero[1]), min(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 작은 포인트
            #(max(nzero[1]), max(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 큰 포인트
            x = min(nzero[1])
            y = min(nzero[0])
            w = max(nzero[1]) - x
            h = max(nzero[0]) - y
            #rectangle: pt1(min(nzero[1]),min(nzero[0])), pt2(max(nzero[1]), max(nzero[0]) 기준으로 사각형 프레임을 만들어줌.            
            cv2.rectangle(draw, (x, y),(w, h), (0, 255, 0), 2)                         
            #(0, 255, 0): 사각형을 그릴 색상 값 #2 : thickness 
                                              
            cv2.putText(draw, "Motion detected!!", (10, 30),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
            cv2.putText(draw,datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(25,draw.shape[0]-50),
                cv2.cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            #save image
            cv2.imwrite("detect_capture/detect_img_%d_%d.jpg"%(count, count2),draw)            

        #영상을 원본으로 복구(배열을 다시 앞으로 붙임,그레이스케일을 BGR 색상 이미지로 반환)
        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        cv2.putText(stacked, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (25, stacked.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow('Motion_detect_tracing', stacked)
        
       ###############################################

        #video recording save                     
        #outVideo = 'test_videos/test_video.avi' 
        #w = round(camera.get(cv2.CAP_PROP_FRAME_WIDTH))          
        #h = round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #stacked = cv2.resize(stacked,(w,h))
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')              
        #outVideo = cv2.VideoWriter(outVideo, fourcc, fps, (w,h))
        #outVideo.write(stacked)   
        
        a = b
        b = c     
        key = cv2.waitKey(1) & 0xFF
        #종료를 위한 명령어 "q"
        if key ==ord("q"):
            break
camera.release()
cv2.destroyAllWindows()           