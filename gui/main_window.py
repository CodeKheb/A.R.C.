from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

import cv2
import core.audio as audio

class MainWindow(QMainWindow):
    def __init__(self, camera_callback):
        super().__init__()

        self.camera_callback = camera_callback

        self.setWindowTitle("A.R.C.")
        self.resize(900, 700)

        self.video_label = QLabel("Camera Feed")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("A.R.C. Running")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame = self.camera_callback()

        if frame is None:
            return

        if audio.clap_detected:
            self.close()
            audio.clap_detected = False

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb.shape
        bytes_per_line = ch * w

        image = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(image)

        self.video_label.setPixmap(
            pixmap.scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            )
        )
