# 👤 FaceID Attendance System

A real-time face recognition-based attendance system using OpenCV and the `face_recognition` library. It recognizes known faces from a webcam feed and logs their attendance automatically — both locally (in a CSV file) and remotely using **Supabase**, a scalable open-source backend.

---

## 📌 Features

- Live face recognition using webcam
- Attendance logging with timestamp
- Automatically prevents duplicate entries for the same session
- Stores attendance both locally (`Attendance.csv`) and remotely via Supabase
- Clean and modular code

---

## 🛠️ Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- face_recognition
- NumPy
- Pandas
- `supabase` Python client (`supabase-py`)


---
## ▶️ How to Use

Follow these steps in **order** to set up and run the system correctly:

---

### 1️⃣ Add Training Images

- Place clear, front-facing photos of each person inside the `Images/` folder.
- Make sure the **filename matches the person’s name**, as it will be used as the label.
### 2️⃣ Encode Faces
Run the face encoder to process all training images:
### 3️⃣ Start Attendance System
