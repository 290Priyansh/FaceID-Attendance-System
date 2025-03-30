import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
from supabase import create_client
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create a client to interact with Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Import functions and student IDs from Encodegenrator script
from openCV.Face_recog.Encodegenrator import encodeListKnown, encodeListKnownWithIds, studentIds

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

# Load background image
imgBg = cv2.imread("D:\\python\\openCV\\Face_recog\\Resources\\Background.png")

# Load mode images from folder
folderModePath = "Resources\\Modes"
ModePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in ModePathList]

# Load precomputed face encodings from a file
print("loading encode file....")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("encode file loaded!")

# Initialize variables
modeType = 0
counter = 0
id = -1
imgStudent = []
last_detected_id = None
last_detected_time = None

while True:
    # Capture frame from webcam
    success, img = cap.read()

    # Resize image for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Overlay webcam feed onto the background image
    imgBg[162:162 + 480, 55:55 + 640] = img
    imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # Compare detected face with known encodings
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)  # Get best match

            if matches[matchIndex]:
                # Extract bounding box and draw around the detected face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBg = cvzone.cornerRect(imgBg, bbox, rt=0)
                id = studentIds[matchIndex]
                print(id)

                # Change mode when a face is detected
                if counter == 0:
                    if modeType != 1:
                        cvzone.putTextRect(imgBg, "loading", (275, 400))
                        cv2.imshow("face attendance", imgBg)
                        cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Fetch student details from Supabase
                response = supabase.table("students").select("*").eq("id", id).execute()
                studentInfo = response.data[0]

                # Fetch student profile image from Supabase storage
                image_path = f"{id}.png"
                response = supabase.storage.from_("students-files").download(image_path)
                array = np.frombuffer(response, np.uint8)
                imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

                if studentInfo:
                    last_attendance_time = studentInfo.get('last_attendance_time', None)
                    if last_attendance_time:
                        last_attendance_time = last_attendance_time.rstrip('Z')
                        datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%dT%H:%M:%S.%f")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()

                        if secondsElapsed >= 30:
                            # Update attendance count
                            current_attendance = studentInfo["total_attendance"]
                            new_attendance = current_attendance + 1
                            supabase.table("students").update({"total_attendance": new_attendance}).eq("id",
                                                                                                       id).execute()
                            modeType = 3
                            counter = 0
                            imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                        else:
                            modeType = 4
                            counter = 0
                            imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType != 3:
                if 20 < counter < 30:
                    modeType = 2
                    imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 30:
                    # Display student details on the screen
                    cv2.putText(imgBg, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.putText(imgBg, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                                (255, 255, 255), 1)
                    cv2.putText(imgBg, str(studentInfo['id']), (1006, 493), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                                (255, 255, 255), 1)

                    imgStudent = cv2.resize(imgStudent, (216, 216))
                    imgBg[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

    else:
        if counter > 0:
            counter += 1
            if counter >= 30:
                counter = 0
                modeType = 0
                studentInfo = []
                imgStudent = []
                imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    # Exit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imshow("face attendance", imgBg)
cv2.waitKey(1)
