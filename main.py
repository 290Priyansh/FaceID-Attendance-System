# import os
# import pickle
# import cv2
# import face_recognition
# import numpy as np
# import cvzone
# from supabase import create_client
# from datetime import datetime
# from dotenv import load_dotenv
# import sys
# module_path = r"D:\\python\\openCV\\Face_recog"
# sys.path.append(module_path)
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Get Supabase credentials from environment variables
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
#
# # Create a client to interact with Supabase
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#
# # Import functions and student IDs from Encodegenrator script
# from Face_recog.Encodegenrator import encodeListKnown, encodeListKnownWithIds, studentIds
#
# # Initialize webcam capture
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)  # Set width
# cap.set(4, 480)  # Set height
#
# # Load background image
# imgBg = cv2.imread("D:\\python\\openCV\\Face_recog\\Resources\\Background.png")
#
# # Load mode images from folder
# folderModePath = "Resources\\Modes"
# ModePathList = os.listdir(folderModePath)
# imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in ModePathList]
#
# # Load precomputed face encodings from a file
# print("loading encode file....")
# file = open("EncodeFile.p", 'rb')
# encodeListKnownWithIds = pickle.load(file)
# file.close()
# encodeListKnown, studentIds = encodeListKnownWithIds
# print("encode file loaded!")
#
# # Initialize variables
# modeType = 0
# counter = 0
# id = -1
# imgStudent = []
# last_detected_id = None
# last_detected_time = None
#
# while True:
#     # Capture frame from webcam
#     success, img = cap.read()
#
#     # Resize image for faster processing
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#     # Detect faces and encode them
#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
#
#     # Overlay webcam feed onto the background image
#     imgBg[162:162 + 480, 55:55 + 640] = img
#     imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#
#     if faceCurFrame:
#         for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#             # Compare detected face with known encodings
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             matchIndex = np.argmin(faceDis)  # Get best match
#
#             if matches[matchIndex]:
#                 # Extract bounding box and draw around the detected face
#                 y1, x2, y2, x1 = faceLoc
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#                 bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#                 imgBg = cvzone.cornerRect(imgBg, bbox, rt=0)
#                 id = studentIds[matchIndex]
#                 print(id)
#
#                 # Change mode when a face is detected
#                 if counter == 0:
#                     if modeType != 1:
#                         cvzone.putTextRect(imgBg, "loading", (275, 400))
#                         cv2.imshow("face attendance", imgBg)
#                         cv2.waitKey(1)
#                     counter = 1
#                     modeType = 1
#
#         if counter != 0:
#             if counter == 1:
#                 # Fetch student details from Supabase
#                 response = supabase.table("students").select("*").eq("id", id).execute()
#                 studentInfo = response.data[0]
#
#                 # Fetch student profile image from Supabase storage
#                 image_path = f"{id}.png"
#                 response = supabase.storage.from_("students-files").download(image_path)
#                 array = np.frombuffer(response, np.uint8)
#                 imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
#
#                 if studentInfo:
#                     last_attendance_time = studentInfo.get('last_attendance_time', None)
#                     if last_attendance_time:
#                         last_attendance_time = last_attendance_time.rstrip('Z')
#                         datetimeObject = datetime.strptime(last_attendance_time, "%Y-%m-%dT%H:%M:%S.%f")
#                         secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
#
#                         if secondsElapsed >= 30:
#                             # Update attendance count
#                             current_attendance = studentInfo["total_attendance"]
#                             new_attendance = current_attendance + 1
#                             supabase.table("students").update({"total_attendance": new_attendance}).eq("id",
#                                                                                                        id).execute()
#                             modeType = 3
#                             counter = 0
#                             imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#                         else:
#                             modeType = 4
#                             counter = 0
#                             imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#             if modeType != 3:
#                 if 20 < counter < 30:
#                     modeType = 2
#                     imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#
#                 if counter <= 30:
#                     # Display student details on the screen
#                     cv2.putText(imgBg, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_TRIPLEX, 1,
#                                 (255, 255, 255), 1)
#                     cv2.putText(imgBg, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
#                                 (255, 255, 255), 1)
#                     cv2.putText(imgBg, str(studentInfo['id']), (1006, 493), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
#                                 (255, 255, 255), 1)
#
#                     imgStudent = cv2.resize(imgStudent, (216, 216))
#                     imgBg[175:175 + 216, 909:909 + 216] = imgStudent
#
#                 counter += 1
#
#     else:
#         if counter > 0:
#             counter += 1
#             if counter >= 30:
#                 counter = 0
#                 modeType = 0
#                 studentInfo = []
#                 imgStudent = []
#                 imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#
#     # Exit the program when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.imshow("face attendance", imgBg)
# cv2.waitKey(1)

import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
from supabase import create_client
from datetime import datetime
from dotenv import load_dotenv
import sys

# --- Path Configuration ---
module_path = r"D:\\python\\openCV"
sys.path.append(module_path)

# --- Load Environment Variables ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"Loaded SUPABASE_URL: {SUPABASE_URL}")
print(f"Loaded SUPABASE_KEY: {'*' * len(SUPABASE_KEY) if SUPABASE_KEY else 'None'}")

# --- Supabase Client Initialization ---
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client created successfully.")
except Exception as e:
    print(f"ERROR: Failed to create Supabase client: {e}")
    print("Please check your SUPABASE_URL and SUPABASE_KEY in the .env file and your internet connection.")
    sys.exit(1)

# --- Import Encodings ---
try:
    from Face_recog.Encodegenrator import encodeListKnown, encodeListKnownWithIds, studentIds

    print("Encodegenrator imported successfully.")
except ImportError as e:
    print(f"ERROR: Could not import Encodegenrator: {e}")
    print(
        f"Please ensure the directory '{module_path}\\Face_recog\\Encodegenrator.py' exists and is correctly structured.")
    sys.exit(1)

# --- Webcam Initialization ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open webcam. Check if camera is connected or in use by another application.")
    sys.exit(1)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height
print("Webcam initialized.")

# --- Load Resources ---
BASE_RESOURCE_PATH = "D:\\python\\openCV\\Face_recog\\Resources"

imgBg = cv2.imread(os.path.join(BASE_RESOURCE_PATH, "Background.png"))
if imgBg is None:
    print(
        f"ERROR: Could not load Background.png. Check file path: {os.path.join(BASE_RESOURCE_PATH, 'Background.png')}")
    sys.exit(1)
print("Background image loaded.")

folderModePath = os.path.join(BASE_RESOURCE_PATH, "Modes")
ModePathList = os.listdir(folderModePath)
imgModeList = []
for path in ModePathList:
    full_path = os.path.join(folderModePath, path)
    img = cv2.imread(full_path)
    if img is None:
        print(f"WARNING: Could not load mode image: {full_path}")
    imgModeList.append(img)

if not imgModeList or any(img is None for img in imgModeList):
    print("ERROR: Some or all mode images failed to load. Check 'Resources\\Modes' folder content.")
    sys.exit(1)
print(f"{len(imgModeList)} mode images loaded.")

# --- Load Precomputed Face Encodings ---
print("Loading encode file....")
encode_file_path = "D:\\python\\openCV\\Face_recog\\EncodeFile.p"
try:
    with open(encode_file_path, 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode file loaded!")
except FileNotFoundError:
    print(f"ERROR: EncodeFile.p not found at {encode_file_path}. Run Encodegenrator.py first!")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Failed to load EncodeFile.p: {e}")
    sys.exit(1)

# --- Initialize Variables ---
modeType = 0
counter = 0
id = -1
imgStudent = None  # Initialize as None
studentInfo = {}  # Initialize as an empty dictionary

print("Starting main loop...")

# --- Main Loop ---
while True:
    success, img = cap.read()
    if not success:
        print("ERROR: Failed to read frame from camera. Exiting loop.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Overlay webcam feed onto the background image
    imgBg[162:162 + 480, 55:55 + 640] = img

    # Ensure modeType is within bounds and image is not None before drawing
    if 0 <= modeType < len(imgModeList) and imgModeList[modeType] is not None:
        imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        print(f"WARNING: modeType {modeType} is out of bounds or image is None. Defaulting to mode 0.")
        modeType = 0  # Fallback to default mode
        if 0 <= modeType < len(imgModeList) and imgModeList[modeType] is not None:
            imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    print(f"\n--- Frame Loop Start --- Mode: {modeType}, Counter: {counter}, Faces: {len(faceCurFrame)}")

    if faceCurFrame:  # A face (or faces) is detected in the current frame
        print(f"Face detected in frame.")
        # We only process the first detected face for simplicity in this loop
        # If multiple faces are present, the one with the best match will be processed.
        # This loop is mainly for drawing bbox and identifying 'id'
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                # Extract bounding box and draw around the detected face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBg = cvzone.cornerRect(imgBg, bbox, rt=0)
                # Only update 'id' if 'counter' is 0 (new detection) or we are in loading/display mode
                # This prevents 'id' from changing if multiple faces are present after info is displayed
                if counter == 0 or modeType in [1, 2]:
                    id = studentIds[matchIndex]
                print(f"Matched ID: {id}. Distance: {faceDis[matchIndex]:.2f}")
                # Assuming we care about the first matched ID, break after finding it
                # If you want to process ALL faces, remove this break.
                break

        # --- Logic for handling detected and matched face ---
        if counter == 0:  # This means a new face has been detected (or previous process finished/reset)
            print("Counter is 0 (new detection). Setting initial state for data fetch.")
            cvzone.putTextRect(imgBg, "loading...", (275, 400), scale=2, thickness=2, offset=15)
            cv2.imshow("face attendance", imgBg)  # Show loading text immediately
            cv2.waitKey(1)  # Short delay to allow display update

            # Reset studentInfo and imgStudent before fetching new data for the detected 'id'
            studentInfo = {}
            imgStudent = None

            # Set mode to 1 (loading) and counter to 1 (indicating data fetch in next loop)
            modeType = 1
            counter = 1
            print(f"DEBUG: Initial detection. Mode: {modeType}, Counter: {counter}")

        elif counter == 1:  # We are in Mode 1 (loading), time to fetch data
            print(f"Counter is 1 (fetching data). Attempting to fetch details for ID: {id}")
            # Fetch student details from Supabase
            try:
                response = supabase.table("students").select("*").eq("id", id).execute()
                if response.data and len(response.data) > 0:
                    studentInfo = response.data[0]
                    print(f"Successfully fetched studentInfo: {studentInfo.get('name', 'N/A')}")
                else:
                    print(f"WARNING: No student found with ID: {id} in Supabase. Resetting.")
                    modeType = 0
                    counter = 0
                    studentInfo = {}
                    imgStudent = None
                    continue  # Skip remaining logic for this frame if no student found
            except Exception as e:
                print(f"ERROR: Supabase data fetch failed for ID {id}: {e}")
                print("Possible network issue, incorrect Supabase URL/Key, or table/RLS problem.")
                modeType = 0
                counter = 0
                studentInfo = {}
                imgStudent = None
                continue  # Skip remaining logic for this frame

            # Fetch student profile image from Supabase storage
            print(f"Attempting to download image for ID: {id}.png")
            try:
                image_path = f"{id}.png"
                response_storage = supabase.storage.from_("students-files").download(image_path)
                if response_storage:
                    array = np.frombuffer(response_storage, np.uint8)
                    temp_img_student = cv2.imdecode(array, cv2.IMREAD_COLOR)
                    if temp_img_student is None or temp_img_student.size == 0:
                        print(f"WARNING: cv2.imdecode returned None/empty for {id}.png. Using placeholder.")
                        imgStudent = np.zeros((216, 216, 3), np.uint8)  # Fallback to black image
                    else:
                        imgStudent = temp_img_student
                        print(f"Successfully downloaded and decoded image for {id}.png. Shape: {imgStudent.shape}")
                else:
                    print(f"WARNING: Supabase storage download returned empty for {id}.png. File might not exist.")
                    imgStudent = np.zeros((216, 216, 3), np.uint8)  # Fallback to black image
            except Exception as e:
                print(f"ERROR: Supabase storage download failed for {id}.png: {e}")
                imgStudent = np.zeros((216, 216, 3), np.uint8)  # Fallback to black image

            # After successful data and image fetch, transition to display info mode
            modeType = 2  # Transition to display info mode
            counter = 2  # Start counter for display frames
            print(f"DEBUG: Data fetched. Transitioning to Mode 2 (Display). Counter: {counter}")

        elif modeType == 2:  # We are in the display info mode
            # Display student details every frame while in Mode 2
            if studentInfo and imgStudent is not None and imgStudent.shape[0] > 0 and imgStudent.shape[1] > 0:
                cv2.putText(imgBg, str(studentInfo.get('total_attendance', 'N/A')), (867, 140),
                            cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0), 1)
                cv2.putText(imgBg, str(studentInfo.get('major', 'N/A')), (1006, 550), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                            (0,0,0), 1)
                cv2.putText(imgBg, str(studentInfo.get('id', 'N/A')), (1006, 500), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                            (0,0,0), 1) # Adjusted for Black color
                cv2.putText(imgBg, str(studentInfo.get('name', 'N/A')), (885, 470), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                            (0,0,0), 1) # Adjusted for Black color
                cv2.putText(imgBg, str(studentInfo.get('standing', 'N/A')), (910, 625), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                            (0,0,0), 1) # Adjusted for Black color
                cv2.putText(imgBg, str(studentInfo.get('starting_year', 'N/A')), (1025, 625), cv2.FONT_HERSHEY_TRIPLEX,
                            0.6, (0,0,0), 1) # Adjusted for Black color

                try:
                    imgStudent_resized = cv2.resize(imgStudent, (216, 216))
                    imgBg[175:175 + 216, 909:909 + 216] = imgStudent_resized
                except Exception as e:
                    print(f"ERROR: Could not resize or place student image on background during display: {e}")
            else:
                print("WARNING: Student info or image not fully loaded for display in Mode 2. Resetting.")
                modeType = 0
                counter = 0
                studentInfo = {}
                imgStudent = None
                continue  # Skip to next frame

            # Define how long to show the info (e.g., 30 frames for ~1 second at 30 FPS)
            DISPLAY_FRAMES_COUNT = 30  # Adjust this value as needed for display duration
            print(f"DEBUG_DISPLAY: Current Mode 2 counter: {counter} / {DISPLAY_FRAMES_COUNT}")
            if counter >= DISPLAY_FRAMES_COUNT:
                print(f"DEBUG_DISPLAY: Display time elapsed ({counter} frames). Proceeding to attendance marking logic.")
                # --- Attendance Marking Logic (executes ONLY once after display duration) ---
                if studentInfo:
                    last_attendance_db = studentInfo.get('last_attendance', None)
                    print(f"DEBUG_ATTENDANCE: Last attendance time from DB ('last_attendance'): {last_attendance_db}")

                    if last_attendance_db:
                        try:
                            # Parse Supabase timestamp, handling 'Z' and optional microseconds
                            time_str_to_parse = last_attendance_db.rstrip('Z')
                            if '.' in time_str_to_parse:
                                datetimeObject = datetime.strptime(time_str_to_parse.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            else:
                                datetimeObject = datetime.strptime(time_str_to_parse, "%Y-%m-%dT%H:%M:%S")

                            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                            print(f"DEBUG_ATTENDANCE: Seconds elapsed since last attendance: {secondsElapsed:.2f}")

                            ATTENDANCE_COOLDOWN_SECONDS = 30  # Cooldown period for attendance marking
                            if secondsElapsed >= ATTENDANCE_COOLDOWN_SECONDS:
                                print("DEBUG_ATTENDANCE: Eligible for attendance update. Updating...")
                                current_attendance = studentInfo.get("total_attendance", 0)
                                new_attendance = current_attendance + 1
                                try:
                                    supabase.table("students").update({
                                        "total_attendance": new_attendance,
                                        "last_attendance": datetime.now().isoformat(timespec='milliseconds') + 'Z'
                                    }).eq("id", id).execute()
                                    print(f"DEBUG_ATTENDANCE: Attendance updated successfully for ID {id}. New count: {new_attendance}")
                                    modeType = 3  # Mode for "Attendance Marked"
                                    counter = 0  # Reset for next detection
                                except Exception as e:
                                    print(f"ERROR: Failed to update attendance in Supabase: {e}")
                                    modeType = 0  # Reset on error
                                    counter = 0
                            else:  # Not enough time passed since last attendance
                                print(
                                    f"DEBUG_ATTENDANCE: Attendance already marked recently (<{ATTENDANCE_COOLDOWN_SECONDS}s). Not updating.")
                                modeType = 4  # Mode for "Already Marked"
                                counter = 0  # Reset for next detection
                        except ValueError as ve:
                            print(
                                f"ERROR: Could not parse last_attendance_time '{last_attendance_db}': {ve}. Allowing update.")
                            # If parsing fails, allow update to fix potential bad data
                            modeType = 0
                            counter = 0
                        except Exception as e:
                            print(f"ERROR: General error in attendance time calculation for {id}: {e}")
                            modeType = 0
                            counter = 0
                    else:  # 'last_attendance' is None (first time attendance for this student)
                        print("DEBUG_ATTENDANCE: last_attendance is None. Proceeding to mark first attendance.")
                        current_attendance = studentInfo.get("total_attendance", 0)
                        new_attendance = current_attendance + 1
                        try:
                            supabase.table("students").update({
                                "total_attendance": new_attendance,
                                "last_attendance": datetime.now().isoformat(timespec='milliseconds') + 'Z'
                            }).eq("id", id).execute()
                            print(f"DEBUG_ATTENDANCE: First attendance marked for ID {id}. Count: {new_attendance}.")
                            modeType = 3  # Attendance Marked
                            counter = 0  # Reset for next detection
                        except Exception as e:
                            print(f"ERROR: Failed to mark first attendance in Supabase: {e}")
                            modeType = 0
                            counter = 0
                else:  # studentInfo missing after display duration
                    print("WARNING: studentInfo missing after display duration. Resetting.")
                    modeType = 0
                    counter = 0
                    studentInfo = {}
                    imgStudent = None
            else: # Still in display phase, increment counter
                counter += 1
                # print(f"DEBUG: Counter incremented to {counter} for display duration.") # This can spam the console, removed from previous debug

    else:  # No face detected in the current frame
        if counter > 0:  # If a process was active, continue countdown to reset
            counter += 1
            print(f"No face detected. Counter: {counter}, Mode: {modeType}")
            # Reset after a certain number of frames if no face is detected
            # This allows the "marked" or "already marked" message to stay briefly.
            RESET_COOLDOWN_FRAMES = 50  # Total frames before reset if no face (adjust as needed)
            if counter >= RESET_COOLDOWN_FRAMES:
                print("No face detected for long enough. Resetting to Mode 0.")
                counter = 0
                modeType = 0
                studentInfo = {}
                imgStudent = None
                # Update mode image to default
                if 0 <= modeType < len(imgModeList) and imgModeList[modeType] is not None:
                    imgBg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                else:
                    print(f"WARNING: Cannot update mode image to default for modeType {modeType}")

    # Always show the updated background image
    cv2.imshow("face attendance", imgBg)

    # Exit the program when 'q' is pressed
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        print(" 'q' pressed. Exiting.")
        break

# --- Cleanup ---
cv2.destroyAllWindows()
cap.release()
print("Application shut down cleanly.")