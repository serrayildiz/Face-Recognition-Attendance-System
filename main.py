import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Set up paths and variables
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Function to find encodings for known images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendance in a CSV file
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# Function to send email notification
def send_email_notification(subject, body, recipient_email, attachment_path=None):
    sender_email = 'serrayildiz1@gmail.com'
    sender_password = 'odecsvbwpaigjkwe'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    # Attach an image if provided
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            img = MIMEImage(attachment.read())
            message.attach(img)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

# Initialize face encodings for known images
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Create the main window
window = tk.Tk()
window.title("Face Recognition")
window.geometry("800x600")
window.configure(bg="#F9F9F9")

# Create a label to display the video feed
label = tk.Label(window, bg="#F9F9F9")
label.pack(pady=10)

# Create buttons for starting/stopping the camera and managing the recognition process
cap = None  # Variable to hold the video capture object
authenticated = False  # Authentication status

# Function to start the camera feed and recognition process
def start_camera():
    global cap, authenticated
    if authenticated:
        cap = cv2.VideoCapture(0)

        # Hide the "Start Camera" button
        start_btn.pack_forget()

        # Show the "Stop Camera" and "View Records" buttons
        stop_btn.pack(side=tk.LEFT, padx=10)
        view_btn.pack(side=tk.LEFT, padx=10)
        logout_btn.pack(side=tk.LEFT, padx=10)

        # Show the camera feed
        label.pack()

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                name = "Not Authenticated"  # Default name for unrecognized faces
                faceColor = (0, 0, 255)  # Red color for unrecognized faces

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    faceColor = (0, 255, 0)  # Green color for recognized faces

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), faceColor, 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), faceColor, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                if matches[matchIndex]:
                    markAttendance(name)
                else:
                    # Send email notification for unrecognized faces
                    subject = 'Unrecognized Face Detected'
                    body = f'An unrecognized face was detected at {datetime.now()}'
                    recipient_email = 'serrayildiz1@gmail.com'  # Enter your email address here
                   # attachment_path = 'path_to_attachment/image.jpg'  # Enter the path to the attachment image here
                    send_email_notification(subject, body, recipient_email) #attachment_path

            # Convert the image to PIL format
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)

            # Resize the image to fit the label
            img = img.resize((640, 480), Image.LANCZOS)

            # Convert the image to Tkinter format and display it
            img = ImageTk.PhotoImage(image=img)
            label.config(image=img)
            label.image = img

            # Check for any user input
            window.update_idletasks()
            window.update()

            # Check if the window should be closed
            if not cap.isOpened() or not authenticated:
                stop_camera()
                break

# Function to stop the camera feed and reset the interface
def stop_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None

        # Hide the camera feed label
        label.pack_forget()

        # Hide the "Stop Camera," "View Records," and "Logout" buttons
        stop_btn.pack_forget()
        view_btn.pack_forget()
        logout_btn.pack_forget()

        # Show the "Start Camera" button
        start_btn.pack(side=tk.LEFT, padx=10)

        # Reset authentication status
        authenticated = False

# Function to view attendance records
def view_records():
    os.system('Attendance.csv')

# Function to validate login credentials
def login():
    global authenticated
    username = username_entry.get()
    password = password_entry.get()

    # Add your authentication logic here
    # For simplicity, let's assume the credentials are "admin" and "password"
    if username == "admin" and password == "password":
        authenticated = True
        login_frame.pack_forget()
        start_camera()

    else:
        login_error_label.config(text="Invalid credentials")

# Function to log out
def logout():
    global authenticated
    authenticated = False
    stop_camera()
    login_frame.pack()
    start_btn.pack_forget()

# Create and style the buttons
button_frame = tk.Frame(window, bg="#F9F9F9")
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="Start Camera", command=start_camera, padx=20, pady=10, bg="#4CAF50", fg="#FFFFFF")
stop_btn = tk.Button(button_frame, text="Stop Camera", command=stop_camera, padx=20, pady=10, bg="#F44336", fg="#FFFFFF")
view_btn = tk.Button(button_frame, text="View Records", command=view_records, padx=20, pady=10, bg="#2196F3", fg="#FFFFFF")
logout_btn = tk.Button(button_frame, text="Logout", command=logout, padx=20, pady=10, bg="#FF9800", fg="#FFFFFF")

# Create a frame for the login page
login_frame = tk.Frame(window, bg="#F9F9F9")
login_frame.pack(pady=50)

# Create labels and entry fields for username and password
username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 14), bg="#F9F9F9")
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=("Helvetica", 14))
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 14), bg="#F9F9F9")
password_label.pack(pady=10)
password_entry = tk.Entry(login_frame, font=("Helvetica", 14), show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login, padx=20, pady=10, bg="#4CAF50", fg="#FFFFFF")
login_button.pack(pady=10)

login_error_label = tk.Label(login_frame, text="", font=("Helvetica", 12), fg="red", bg="#F9F9F9")
login_error_label.pack(pady=10)

# Hide the "Start Camera" button initially
start_btn.pack_forget()

# Start the Tkinter event loop
window.mainloop()
