# NOIRcamera 
## motion_detect_tracing

## [install lib]

```pip install opencv-python```

```pip install opencv-contrib-python```

## [Run]
+ Camera connect

``` python -m motion_detect_tracing```

+ Camera disconnect

```python -m motion_detect_tracing -v video.avi```

## [Explanation]
    > 카메라 사용시 "Camera connect!!"
    >
    > 카메라 미사용시 "Camera disconnect!!"
    >
    > 프레임 3개를 서로 비교하여 변화 감지시 움직임을 감지합니다.
    >
    > 종료시 'q' 입력
    >
    >https://picamera.readthedocs.io/en/release-1.13/recipes1.html
    >
    >raspberry pi camera 해설
    >
    >https://potatoggg.tistory.com/192
    >
    >video motion detection capture python
    >
    >https://s-engineer.tistory.com/107
    >
    >video motion detection C++
    >
    >https://hyongdoc.tistory.com/410
    >  
    >video motion detection python




