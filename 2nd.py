import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cv2
import face_recognition
import pandas as pd
from datetime import datetime

# Define the scope and credentials for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Authorize the client
client = gspread.authorize(credentials)

# Open the Google Sheets spreadsheet
spreadsheet = client.open('Your Google Sheets Spreadsheet Name')

# Select the worksheet by name
worksheet = spreadsheet.worksheet('Sheet1')  # Replace 'Sheet1' with the name of your worksheet

# Get all values from the worksheet
student_data = worksheet.get_all_values()

# Load student data into a DataFrame
df = pd.DataFrame(student_data[1:], columns=student_data[0])

# Initialize the attendance system
class Student:
    def __init__(self, roll_no, name):
        self.roll_no = roll_no
        self.name = name
        self.attendance = {}

    def mark_attendance(self, date_time):
        self.attendance[date_time.strftime("%Y-%m-%d %H:%M:%S")] = 'Present'

class AttendanceSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, roll_no, name):
        if roll_no not in self.students:
            self.students[roll_no] = Student(roll_no, name)
            print(f"Student {name} with Roll No. {roll_no} added successfully!")
        else:
            print("Student with this Roll No. already exists!")

    def mark_attendance(self, roll_no, date_time):
        if roll_no in self.students:
            self.students[roll_no].mark_attendance(date_time)
            print(f"Attendance marked for Student with Roll No. {roll_no}")
        else:
            print("Student with this Roll No. does not exist!")

attendance_system = AttendanceSystem()

# Add students from DataFrame
for index, row in df.iterrows():
    attendance_system.add_student(row['Roll No'], row['Name'])

# Capture photo and mark attendance for each student
for roll_no, student in attendance_system.students.items():
    print(f"Please capture photo of {student.name} (Roll No. {roll_no}):")
    input("Press Enter when ready...")

    # Capture photo using webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # Convert the image to RGB format (required by face_recognition library)
    rgb_frame = frame[:, :, ::-1]

    # Detect faces in the captured photo
    face_locations = face_recognition.face_locations(rgb_frame)

    # Recognize student and mark attendance
    if len(face_locations) > 0:
        attendance_system.mark_attendance(roll_no, datetime.now())
        print(f"Attendance marked for {student.name}.")
    else:
        print("No face detected. Skipping attendance marking.")
