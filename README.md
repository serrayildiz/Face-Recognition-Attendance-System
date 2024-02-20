Tabii, işte daha detaylı ve İngilizce olarak yazılmış bir GitHub README örneği:

---

# Face Recognition Attendance System

![Face Recognition](images/face_recognition.png)

## Introduction

This is a comprehensive Face Recognition Attendance System developed in Python. The system utilizes advanced computer vision techniques to detect and recognize faces in real-time. It provides features such as attendance marking, email notifications for unrecognized faces, and a user-friendly graphical interface.

## Features

- **Real-time Face Detection and Recognition**: The system captures live video feed from a camera and identifies known faces based on pre-trained encodings.
- **Attendance Marking**: Recognized faces are marked as present in an attendance CSV file along with timestamps.
- **Email Notifications**: Whenever an unrecognized face is detected, the system sends an email notification with a timestamp and an attached image of the unrecognized face.
- **Graphical User Interface (GUI)**: The system comes with a Tkinter-based GUI for easy interaction and control.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/serrayildiz/Face-Recognition-Attendance-System.git
    ```

2. **Install Dependencies**:

    Navigate to the project directory and install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configuration**:

    - **Camera URL**: Update the `camera_url` variable in the `start_camera()` function of the main script (`main.py`) with the appropriate URL of your camera feed.
    
    - **Email Notification**: Modify the `sender_email`, `sender_password`, and `recipient_email` variables in the `send_email_notification()` function of the main script to configure email notifications.

2. **Run the Application**:

    Execute the main Python script to start the face recognition attendance system:

    ```bash
    python main.py
    ```

3. **Login**:

    Upon running the application, you will be prompted to log in with your credentials. For demonstration purposes, use the username `admin` and the password `password`.

4. **Start Camera**:

    After successful login, click on the "Start Camera" button to begin capturing the video feed and recognizing faces.

5. **View Records**:

    You can view the attendance records by clicking on the "View Records" button. This will open the attendance CSV file containing the marked attendance.

6. **Logout**:

    To logout from the system, click on the "Logout" button.

## Credits

This project was developed by [Serra Yıldız](https://github.com/serrayildiz) 
