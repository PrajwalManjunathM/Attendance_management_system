import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

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

    # Example error message
    error_message = "Updated the data to database and generated graphs"
    window = ErrorWindow(error_message)
    window.exec_()  # Show the dialog modally

    sys.exit(app.exec_())
