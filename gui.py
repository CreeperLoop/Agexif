from exif_reader import ExifReader
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QDialog, QLabel, QScrollArea, QMessageBox, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
formatted_data = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exif Reader GUI")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.file_path_label = QLabel("No image selected.")
        self.file_path_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.file_path_label)

        # Default file path label

        self.image_label = QLabel("Image will be displayed here.")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setFrameStyle(QFrame.Shadow.Sunken | QFrame.Shape.Box)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Default image label placeholder and its frame

        # Create a button
        button1 = QPushButton("Select Image")
        button1.clicked.connect(self.on_select_button_click)
        layout.addWidget(button1)

        button2 = QPushButton("Show EXIF Data")
        button2.clicked.connect(self.showDialog)
        layout.addWidget(button2)

        # button3 = QPushButton("Show EXIF Data (List)")
        # button3.clicked.connect(self.showListDialog)
        # layout.addWidget(button3)
        # List mode removed

        button4 = QPushButton("Show EXIF Data (Table)")
        button4.clicked.connect(self.showTableDialog)
        layout.addWidget(button4)
        central_widget.setLayout(layout)

    def on_select_button_click(self):
        #Using QFileDialog to select an image file
        formatted_data.clear()
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                self.file_path_label.setText(f"Selected Image: {image_path}")
                exif_data = ExifReader(image_path).get_exif_data()
                for tag, value in exif_data.items():
                    if tag != "MakerNote":
                        formatted_data.append(f"{tag}: {value}")
                        # formatted_data is for plain text formatted exif information. 
                print("EXIF data read successfully.")
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)

    def showDialog(self):
        # Show the EXIF data in a dialog
        if formatted_data:
            dialog = infoDialog()
            dialog.show()
            dialog.exec()
        else:
            msgbox = QMessageBox(self)
            msgbox.setIcon(QMessageBox.Icon.Information)
            msgbox.setText("Image not selected. ")
            msgbox.setWindowTitle("Warning")
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox.exec()

    def showTableDialog(self):
        if formatted_data:
            dialog = tableDialog()
            dialog.show()
            dialog.exec()

        else:
            msgbox = QMessageBox(self)
            msgbox.setIcon(QMessageBox.Icon.Information)
            msgbox.setText("Image not selected. ")
            msgbox.setWindowTitle("Warning")
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox.exec()


class infoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXIF Data")
        self.setGeometry(150, 150, 400, 300)
        self.setMinimumSize(300, 200)
        self.setSizeGripEnabled(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(QWidget())
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        for data in formatted_data:
            label = QLabel(data)
            label.setWordWrap(True)
            content_layout.addWidget(label)
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        # Word presentation area, scrollable

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        # Set the main layout for the dialog
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_button)
        main_layout.addWidget(back_button)
        self.setLayout(main_layout)

    def back_button(self):
        self.close()


class tableDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXIF Data (Table Mode)")
        self.setGeometry(150, 150, 400, 300)
        self.setMinimumSize(300, 200)
        self.setSizeGripEnabled(True)
        self.table_widget = QTableWidget()
        self.table_widget.setHorizontalHeaderLabels(["Tag","Value"])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.populate_table()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_widget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_button)
        main_layout.addWidget(back_button)
        self.setLayout(main_layout)

    def populate_table(self):
        global formatted_data
        row = 0
        self.table_widget.setRowCount(len(formatted_data))
        # Set the number of rows
        self.table_widget.setColumnCount(2)
        for data in formatted_data:
            if ":" in data:  # Split the data into key and value
                if row != 0:
                    key, value = data.split(":", 1)
                else:
                    key = "Tag"
                    value = "Value"

                key_item = QTableWidgetItem(key.strip())
                value_item = QTableWidgetItem(value.strip())
                self.table_widget.setItem(row, 0, key_item)
                # Add key to column 0
                self.table_widget.setItem(row, 1, value_item)
                # Add value to column 1
                row += 1

    def back_button(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
