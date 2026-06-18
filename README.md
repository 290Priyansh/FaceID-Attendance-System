# Face Recognition Attendance System

This repository contains a Python application for face recognition based attendance management. The system uses computer vision to detect and identify faces, retrieves student records from a Supabase database, and records attendance with a cooldown mechanism to prevent duplicate entries.

## System Components

* main.py: The primary application script that manages the webcam stream, processes video frames, performs face recognition, interacts with Supabase, and updates the graphical user interface.
* Encodegenrator.py: A utility script to load student images from a local directory, generate face encodings, and save them to a serialized file for the main application.
* AddDataToDatabase.py: A script to initialize the database with student records.
* face_mesh.py: An independent script demonstrating face landmark detection and triangulation using MediaPipe.

## Prerequisites

* Python 3.8 or higher
* A camera or webcam connected to the system
* A Supabase account and project

## Installation and Setup

1. Install the required Python libraries:
```bash
pip install opencv_python face_recognition cvzone numpy supabase python_dotenv mediapipe
```

2. Create a file named .env in the root directory and add the Supabase credentials:
```env
SUPABASE_URL = your_supabase_project_url
SUPABASE_KEY = your_supabase_api_key
```

3. Place student images in a directory named Images. Ensure the image filenames match the student ID numbers, for example, 123456.png.

4. Populate the database table with student records:
```bash
python AddDataToDatabase.py
```

5. Generate the face encodings:
```bash
python Encodegenrator.py
```

6. Run the main application:
```bash
python main.py
```

## Database Schema

The system requires a table named students in the Supabase database with the following fields:

* id (Integer, Primary Key): Unique identifier for each student
* name (Text): Student name
* major (Text): Field of study
* starting_year (Integer): Year of enrollment
* total_attendance (Integer): Number of attended sessions
* standing (Text): Academic standing grade
* last_attendance (Timestamp): Timestamp of the last recorded attendance

Additionally, a storage bucket named students-files is required to store the student profile images.

## Project Structure

* Images/ : Directory containing student profile pictures
* Resources/ : Directory containing interface graphics and modes
* EncodeFile.p : Serialized file containing generated face encodings
* main.py : Main program program execution
* Encodegenrator.py : Encoding generation script
* AddDataToDatabase.py : Initial database populating script
* face_mesh.py : Landmark detection script

## How It Works

* When a face is detected in the camera feed, the system generates its encoding and compares it with the local precomputed encodings in EncodeFile.p.
* If a match is found, the system queries the Supabase database for the corresponding student record.
* The system displays the student profile information and image on the graphical interface.
* The system checks the last attendance timestamp. If the elapsed time exceeds the cooldown threshold (set to 30 seconds), the system increments the attendance count and updates the record in the database.
