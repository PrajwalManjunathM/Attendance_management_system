import sys
import cv2
import pickle
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout, QGridLayout, QDialog, QScrollArea, QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import sys
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView


from imutils.video import FPS
import face_recognition
import imutils
import csv
import smtplib
from datetime import date
import time
import pyautogui
import pywhatkit as kit
from datetime import datetime
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF

Attendance_percentage  = None
A_dict = {}
nandini_PN = '+918867256458'
lakshmidevi_PN = '+919886827455'
shrutika_PN = '+917795005711'
gayatri_PN = '+916363939138'

##########################

shrutika_EM = 'shrutikavijaynaiknaik@gmail.com'
nandini_EM = 'nandinikokane08@gmail.com'
lakshmidevi_EM = 'laxmikumawat687@gmail.com'
gayatri_EM = 'gayatrishirodkar592@gmail.com'

#######################
message = 'Your child is absent for the class'
today = datetime.today().strftime('%d-%m-%Y')

class AttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Attendance Management System")
        self.setGeometry(100, 100, 800, 600)

        # Apply styles
        self.apply_styles()

        # Load face recognition model
        self.encodingsP = "encodings.pickle"
        self.cascade = "haarcascade_frontalface_default.xml"
        self.data = pickle.loads(open(self.encodingsP, "rb").read())
        self.detector = cv2.CascadeClassifier(self.cascade)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Navigation bar
        self.nav_bar = QHBoxLayout()
        self.main_layout.addLayout(self.nav_bar)

        # Buttons for navigation
        self.attendance_button = QPushButton("Attendance")
        self.nav_bar.addWidget(self.attendance_button)
        self.attendance_button.clicked.connect(self.show_attendance_page)

        self.second_button = QPushButton("Update Attendance")
        self.nav_bar.addWidget(self.second_button)
        self.second_button.clicked.connect(self.generate_graph)

        self.third_button = QPushButton("Attendance analysis")
        self.nav_bar.addWidget(self.third_button)
        self.third_button.clicked.connect(self.show_image_window)

        # Pages container
        self.pages = QVBoxLayout()
        self.main_layout.addLayout(self.pages)

        # Attendance page
        self.attendance_page = QWidget()
        self.attendance_layout = QVBoxLayout(self.attendance_page)

        # Buttons on attendance page
        self.start_button = QPushButton("Start Attendance")
        self.stop_button = QPushButton("Stop Attendance")
        self.start_camera_button = QPushButton("Start Camera")
        self.capture_button = QPushButton("Capture Image")
        self.stop_camera_button = QPushButton("Stop Camera")

        self.attendance_layout.addWidget(self.start_button)
        self.attendance_layout.addWidget(self.stop_button)
        self.attendance_layout.addWidget(self.start_camera_button)
        self.attendance_layout.addWidget(self.capture_button)
        self.attendance_layout.addWidget(self.stop_camera_button)

        # Initial state
        self.start_camera_button.setEnabled(False)
        self.capture_button.setEnabled(False)
        self.stop_camera_button.setEnabled(False)

        # Connections
        self.start_button.clicked.connect(self.enable_camera_controls)
        self.stop_button.clicked.connect(self.stop_attendance)
        self.start_camera_button.clicked.connect(self.start_camera)
        self.capture_button.clicked.connect(self.capture_image)
        self.stop_camera_button.clicked.connect(self.stop_camera)

        self.camera_active = False
        self.cap = None

        # Image label for video feed
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)  # Set fixed size for the label
        self.image_label.setStyleSheet("background-color: #cccccc;")  # Placeholder color
        self.attendance_layout.addWidget(self.image_label)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #f5f5f5;
                background-image: url('image.jpg'); /* Replace with your image path */
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover; /* Ensures the image scales to fit */
            }}
            QPushButton {{
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
            QLabel {{
                font-size: 16px;
                color: #333333;
                margin: 10px;
            }}
            QWidget {{
                font-family: Arial, sans-serif;
            }}
        """)

    def enable_camera_controls(self):
        self.start_camera_button.setEnabled(True)
        self.capture_button.setEnabled(True)
        self.stop_camera_button.setEnabled(True)

    def generate_graph(self):
        global Attendance_percentage
        # File name
        file_name = "Attendace_simulated.csv"

        # Open the CSV file and read rows
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Convert reader to a list of rows
            row_count = len(rows)
            column_count = len(rows[0]) if rows else 0  # Check columns only if there are rows

        rows = rows[1:]

        for i in rows:
            global Attendance_percentage
            attendance_data = {}

            # File name
            file_name = "Attendace_simulated.csv"
            # Open the CSV file and read rows
            with open(file_name, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)  # Convert reader to a list of rows
                row_count = len(rows)
                column_count = len(rows[0]) if rows else 0  # Check columns only if there are rows

            for data in rows[1:]:
                # Extract name and attendance data
                name = data[0]
                attendance = data[1:]

                # Calculate attendance percentage
                present_count = attendance.count('1')
                total_days = len(attendance)
                attendance_percentage = (present_count / total_days) * 100

                # Add to dictionary
                attendance_data[name] = round(attendance_percentage, 2)

            Attendance_percentage = attendance_data

            # Extract the name and values
            name = i[0]
            values = i[1:]

            # Count ones and zeros
            ones = values.count('1')
            zeros = values.count('0')

            # Generate the dictionary
            result = {'name': name, 'ones': ones, 'zeros': zeros}

            total = ones + zeros
            categories = ['Days Present', 'Days Absent', 'Total number of days']
            values = [ones, zeros, total]
            plt.bar(categories, values)
            plt.title(name.upper())

            # Save the graph as an image file
            output_path = name + '.png'
            plt.savefig(output_path, format='png')
            # time.sleep(2)
            Attendance_percentage[name] = (ones / total) * 100
        print('Graphs generated')
        # Example error message
        error_message = "Updated the data to database and generated graphs"
        self.Error_Window = ErrorWindow(error_message)
        self.Error_Window.show()


    def show_attendance_page(self):
        # Clear previous page and show attendance page
        self.clear_pages()
        self.pages.addWidget(self.attendance_page)

    def clear_pages(self):
        while self.pages.count():
            child = self.pages.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def send_email(self,id):
        today = date.today()

        # Email details
        sender_email = "alertcollege00@gmail.com"
        receiver_email = id
        app_password = "ckol gopy lssb ektu"

        subject = "Regarding College Attendance"
        body = "Dear sir/madam, \n \nThis is to inform you that your child did not attend college today dated: " + str(
            today) + " \n kindly look into this and update. \n\n Regards, \n Nippani College Management"

        # SMTP setup
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as s:
                s.starttls()
                s.login(sender_email, app_password)
                s.sendmail(
                    sender_email,
                    receiver_email,
                    f"Subject: {subject}\n\n{body}"
                )
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error:{e}")

    def enable_camera_controls(self):
        self.start_camera_button.setEnabled(True)
        self.capture_button.setEnabled(True)
        self.stop_camera_button.setEnabled(True)

    def start_camera(self):
        if not self.camera_active:
            self.cap = cv2.VideoCapture(0)
            self.camera_active = True
            self.display_camera_feed()

    def send_whatsapp_message_now(self,phone_number, message):
        kit.sendwhatmsg_instantly(phone_number, message)
        time.sleep(10)  # Delay between messages to prevent being flagged as spam
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(2)
        print("Messages sent successfully!")

    def display_camera_feed(self):
        if self.cap.isOpened() and self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to QPixmap for display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            QApplication.processEvents()
            self.start_camera_button.setEnabled(False)
            QTimer.singleShot(30, self.display_camera_feed)

    def capture_image(self):
        if self.cap is None or not self.cap.isOpened():
            # If the camera is not opened or has been released, start the camera
            self.start_camera()

        if self.cap.isOpened() and self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                try:
                    # Get prediction from the model
                    name = self.send_to_model(frame)
                    self.image_label.setText(f"Prediction: {name}")
                except Exception as e:
                    print(f"Error during prediction: {e}")
                    self.image_label.setText("Error in prediction")
            else:
                print("Failed to capture image")
                self.image_label.setText("Failed to capture image")

    def show_image_window(self):
        # Create a new window
        self.image_window = ImageWindow()
        self.image_window.show()

    def stop_camera(self):
        self.camera_active = False
        if self.cap is not None:
            self.cap.release()
        self.image_label.clear()
        self.start_camera_button.setEnabled(True)

    def update_csv(self):
        global today
        # File name
        file_name = "Attendace_simulated.csv"
        # Open the CSV file and read rows
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Convert reader to a list of rows
            row_count = len(rows)
            column_count = len(rows[0]) if rows else 0  # Check columns only if there are rows
        # print(rows)
        # print(row_count)
        # print(column_count)

        rows[0].append(today)

        try:
            if A_dict['nandini'] == '1':
                rows[1].append(1)
        except:
            rows[1].append(0)

        try:
            if A_dict['shrutika'] == '1':
                rows[2].append(1)
        except:
            rows[2].append(0)

        try:
            if A_dict['gayatri'] == '1':
                rows[3].append(1)
        except:
            rows[3].append(0)

        try:
            if A_dict['lakshmidevi'] == '1':
                rows[4].append(1)
        except:
            rows[4].append(0)

        try:
            if A_dict['faisal'] == '1':
                rows[5].append(1)
        except:
            rows[5].append(0)

        try:
            if A_dict['prajwal'] == '1':
                rows[6].append(1)
        except:
            rows[6].append(0)

        # Write the updated rows back to the file
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print('CSV Updated')

    def send_to_model(self, frame):
        global A_dict

        """Recognize face in the given frame."""
        # Resize frame for faster processing
        frame = imutils.resize(frame, width=500)

        # Convert frame to grayscale and RGB
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the grayscale frame
        rects = self.detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
        )
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # Get facial encodings for detected faces
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(self.data["encodings"], encoding)
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)

            names.append(name)

        # Return the first recognized name or Unknown
        A_dict[names[0]] = '1'
        print(names[0])
        self.attendance_window = AttendanceWindow(names[0])
        self.attendance_window.show()

    def stop_attendance(self):
        global A_dict
        print(A_dict)
        try:
            if A_dict['faisal'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(nandini_PN, message)
            self.send_email(nandini_EM)

        try:
            if A_dict['prajwal'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(nandini_PN, message)
            self.send_email(nandini_EM)

        try:
            if A_dict['nandini'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(nandini_PN, message)
            self.send_email(nandini_EM)

        try:
            if A_dict['shrutika'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(shrutika_PN, message)
            self.send_email(shrutika_EM)

        try:
            if A_dict['lakshmidevi'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(lakshmidevi_PN, message)
            self.send_email(lakshmidevi_EM)

        try:
            if A_dict['gayatri'] == 1:
                pass
        except:
            self.send_whatsapp_message_now(gayatri_PN, message)
            self.send_email(gayatri_EM)

        self.update_csv()
        A_dict = {}



class ImageWindow(QWidget):
    def __init__(self):
        global Attendance_percentage
        super().__init__()
        self.setWindowTitle("Image Window")
        self.showMaximized()  # Open the window maximized

        # Main layout for the window
        main_layout = QVBoxLayout(self)

        # Add a title at the top
        title_label = QLabel("Monthly Reports")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Widget to hold the grid layout
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)

        # Image paths
        image_paths = [
            "faisal.png", "prajwal.png", "gayatri.png",
            "shrutika.png", "lakshmidevi.png", "nandini.png"
        ]  # Replace with actual image paths

        # Add images in a grid (2 columns and n rows)
        for i, path in enumerate(image_paths):
            pixmap = QPixmap(path)
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            row = i // 2  # Calculate row index
            col = i % 2   # Calculate column index
            grid_layout.addWidget(label, row, col)

        # Set the grid layout to the content widget
        content_widget.setLayout(grid_layout)

        # Add the content widget to the scroll area
        scroll_area.setWidget(content_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # ---------------------- Integration for Attendance Percentage ----------------------

        # Create a section for Attendance Percentage
        attendance_title = QLabel("Attendance Percentage")
        attendance_title.setFont(QFont("Arial", 18, QFont.Bold))
        attendance_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(attendance_title)

        attendance_data = {}

        # File name
        file_name = "Attendace_simulated.csv"
        # Open the CSV file and read rows
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Convert reader to a list of rows
            row_count = len(rows)
            column_count = len(rows[0]) if rows else 0  # Check columns only if there are rows

        for data in rows[1:]:
            # Extract name and attendance data
            name = data[0]
            attendance = data[1:]

            # Calculate attendance percentage
            present_count = attendance.count('1')
            total_days = len(attendance)
            attendance_percentage = (present_count / total_days) * 100

            # Add to dictionary
            attendance_data[name] = round(attendance_percentage, 2)

        Attendance_percentage = attendance_data
        # Create a table widget to display attendance
        attendance_table = QTableWidget()
        attendance_table.setRowCount(len(attendance_data))
        attendance_table.setColumnCount(2)
        attendance_table.setHorizontalHeaderLabels(['Name', 'Attendance (%)'])
        attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with attendance data
        row = 0
        for name, attendance in attendance_data.items():
            attendance_item = QTableWidgetItem(f"{attendance:.2f}")
            # Check attendance percentage and apply color coding
            if attendance < 80:
                attendance_item.setBackground(QColor(255, 0, 0))  # Red for below 80%
            else:
                attendance_item.setBackground(QColor(0, 255, 0))  # Green for 80% and above
            attendance_table.setItem(row, 0, QTableWidgetItem(name))
            attendance_table.setItem(row, 1, attendance_item)
            row += 1

        # Add the attendance table to the main layout
        main_layout.addWidget(attendance_table)

        # ---------------------- Today's Attendance Section ----------------------

        # Create a section for Today's Attendance
        todays_title = QLabel("Today's Attendance")
        todays_title.setFont(QFont("Arial", 18, QFont.Bold))
        todays_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(todays_title)

        # Simulate today's attendance data
        todays_attendance_data = {}

        for data in rows[1:]:
            if data[column_count - 1] == '1':
                todays_attendance_data[data[0]] = "Present"
            elif data[column_count - 1] == '0':
                todays_attendance_data[data[0]] = "Absent"

        # Create a table widget for Today's Attendance
        todays_attendance_table = QTableWidget()
        todays_attendance_table.setRowCount(len(todays_attendance_data))
        todays_attendance_table.setColumnCount(2)
        todays_attendance_table.setHorizontalHeaderLabels(['Name', 'Status'])
        todays_attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with today's attendance data
        row = 0
        for name, status in todays_attendance_data.items():
            status_item = QTableWidgetItem(status)
            # Apply color coding based on status
            if status == "Absent":
                status_item.setBackground(QColor(255, 0, 0))  # Red for absent
            else:
                status_item.setBackground(QColor(0, 255, 0))  # Green for present
            todays_attendance_table.setItem(row, 0, QTableWidgetItem(name))
            todays_attendance_table.setItem(row, 1, status_item)
            row += 1

        # Add the Today's Attendance table to the main layout
        main_layout.addWidget(todays_attendance_table)

        self.setLayout(main_layout)
        print(Attendance_percentage)
class AttendanceWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle("Attendance Confirmation")
        self.resize(300, 150)  # Set initial window size

        # Create a label with the message
        self.label = QLabel(f"Attendance marked for {name}")
        self.label.setStyleSheet("font-size: 16px;")
        self.label.setAlignment(Qt.AlignCenter)

        # Create an OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet("font-size: 14px; padding: 5px;")
        self.ok_button.clicked.connect(self.close)  # Close the window on click

        # Arrange widgets in a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        # Center the window on the screen
        self.center_on_screen()

    def center_on_screen(self):
        # Get the screen's geometry
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

class ErrorWindow(QDialog):
    def __init__(self, error_message):
        super().__init__()
        self.setWindowTitle("Updation Window")
        self.setFixedSize(300, 150)

        # Create layout and widgets
        layout = QVBoxLayout()

        label = QLabel(error_message)
        label.setWordWrap(True)  # Allow text wrapping
        layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.close)  # Close the window on button click
        layout.addWidget(ok_button)

        # Set layout
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceSystem()
    window.showMaximized()
    sys.exit(app.exec_())