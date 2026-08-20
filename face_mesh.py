import cv2
import mediapipe as mp
import time

from mediapipe.python.solutions.drawing_utils import GREEN_COLOR

cap = cv2.VideoCapture('/openCV/Face_recog\Two_people.mp4')
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1,circle_radius=1,color=GREEN_COLOR)

while True:
    success,img = cap.read()
    new_width = 640
    new_height = 500
    resize = cv2.resize(img, (new_width, new_height))

    imgRgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRgb)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(resize,faceLms,
                                  mpFaceMesh.FACEMESH_TESSELATION,drawSpec,drawSpec)
            for idx,lm in enumerate(faceLms.landmark):
                ih,iw,ic = img.shape
                x,y = int(lm.x*iw),int(lm.y*ih)
                print(id,x,y)




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(resize,f'FPS:{int(fps)}',(10,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,0),3)


    cv2.imshow('image',resize)
    cv2.waitKey(1)