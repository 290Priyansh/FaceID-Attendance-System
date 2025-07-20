import cv2
import face_recognition
import pickle
import os

from supabase import create_client


# Initialize Supabase
SUPABASE_URL = "your supabase url"
SUPABASE_KEY = "your supabase key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

bucket_name = "students-files"
folderPath = "Images"
PathList = os.listdir(folderPath)
imgList = []
studentIds = []





# Process images
for path in PathList:
    try:
        img_path = os.path.join(folderPath, path)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Could not read image {path}")
            continue

        imgList.append(img)
        student_id = os.path.splitext(path)[0]
        studentIds.append(student_id)

        # Upload to Supabase
        storage_path = f"profile_pictures/{student_id}/{path}"


    except Exception as e:
        print(f"Error processing {path}: {str(e)}")
        continue


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(img)
            if face_encodings:
                encodeList.append(face_encodings[0])
        except Exception as e:
            print(f"Error encoding image: {str(e)}")
            continue
    return encodeList


print("Encoding started.....")
encodeListKnown = findEncodings(imgList)
if not encodeListKnown:
    raise ValueError("No face encodings were generated - check your images")

encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed!")

# Save encodings
with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)
print("Encodings file saved")
