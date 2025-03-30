from supabase import create_client
SUPABASE_URL = "https://jzixowbqovizmxtvhasj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp6aXhvd2Jxb3Zpem14dHZoYXNqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMwODEwMjYsImV4cCI6MjA1ODY1NzAyNn0.udi-RVP97obIUqO0sb9ONLcYYZeHbrkRWz9Gpkr1DwI"
# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Reference the "students" table (equivalent to db.reference('Students'))
students_table = supabase.table("students")

# Define Student Data
data = [
    {
        "id":111000,
        "name": "Priyansh Vaish",
        "major": "CSE-AIML",
        "starting_year": 2023,
        "total_attendance": 80,
        "standing": "A",
        "last_attendance": "2025-03-27  00:08:30"
    },
    {
        "id":123456,
        "name": "Virat Kholi",
        "major": "CSE-Cyber",
        "starting_year": 2022,
        "total_attendance": 60,
        "standing": "B",
        "last_attendance": "2025-02-27  00:06:30"
    },
    {
        "id": 852741,
        "name": "Emily Blunt",
        "major": "CSE-Core",
        "starting_year": 2024,
        "total_attendance": 75,
        "standing": "A",
        "last_attendance": "2025-03-27  00:10:30"
},
{
        "id": 963852,
        "name": "Elon Musk",
        "major": "CSE-Cloud",
        "starting_year": 2021,
        "total_attendance": 50,
        "standing": "C",
        "last_attendance": "2025-03-27  00:08:30"

}]
response = supabase.table("students").upsert(data).execute()


