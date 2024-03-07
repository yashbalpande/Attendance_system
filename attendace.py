import pandas as pd
import cv2
import face_recognition
from datetime import datetime

class Student:
    def __init__(self, roll_no, name, photo_filename):
        self.roll_no = roll_no
        self.name = name
        self.photo_filename = photo_filename
        self.attendance = {}

    def mark_attendance(self, date_time):
        self.attendance[date_time.strftime("%Y-%m-%d %H:%M:%S")] = 'Present'

class AttendanceSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, roll_no, name, photo_filename):
        if roll_no not in self.students:
            self.students[roll_no] = Student(roll_no, name, photo_filename)
            print(f"Student {name} with Roll No. {roll_no} added successfully!")
        else:
            print("Student with this Roll No. already exists!")

    def mark_attendance(self, roll_no, date_time):
        if roll_no in self.students:
            self.students[roll_no].mark_attendance(date_time)
            print(f"Attendance marked for Student with Roll No. {roll_no} at {date_time}")
        else:
            print("Student Absent with Roll No. {roll_no} at {date_time}")
#   code over here 
            #adding excel sheet for storing data
student_data = pd.read_excel("student_data.xlsx")

#  attendance data
attendance_system = AttendanceSystem()

# Add students excel sheet
for index, row in student_data.iterrows():
    attendance_system.add_student(row['Roll No'], row['Name'], row['Photo Filename'])

#  photo and mark attendance for each student
for roll_no, student in attendance_system.students.items():
    print(f"Please capture photo of {student.name} (Roll No. {roll_no}):")
    input("Press Enter when ready...")
    
    # Capture photo
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    # captured photo
    photo_filename = f"captured_photos/{roll_no}_captured.jpg"
    cv2.imwrite(photo_filename, frame)

    # Load student image and identify 
    student_image = face_recognition.load_image_file(photo_filename)
    student_encoding = face_recognition.face_encodings(student_image)[0]
    detected_student = False

    for roll_no, student in attendance_system.students.items():
        known_encoding = face_recognition.face_encodings(face_recognition.load_image_file(f"student_photos/{student.photo_filename}"))[0]
        results = face_recognition.compare_faces([known_encoding], student_encoding)
        if True in results:
            attendance_system.mark_attendance(roll_no, datetime.now())
            detected_student = True
        

    if not detected_student:
        print("Unknown person detected.")

# Save attendance data to a CSV file (for Final Result)
attendance_data = []
for roll_no, student in attendance_system.students.items():
    for date_time, status in student.attendance.items():
        attendance_data.append({'Roll No': roll_no, 'Name': student.name, 'Date & Time': date_time, 'Status': status})

# Assuming attendance_data is your data
attendance_df = pd.DataFrame(attendance_data)

# Generate current date and time for the file name
current_datetime = datetime.now().strftime("%Y-%m-%d")

# Concatenate the timestamp with the file extension
file_name = f"attendance_{current_datetime}.csv"

# Save DataFrame to CSV with the updated file name
attendance_df.to_csv(file_name, index=False)
