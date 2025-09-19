from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        headers = ["B", "I", "N", "G", "O"]
        for i, letter in enumerate(headers):
            label = QLabel(letter)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 72px;
                font-weight: bold;
            """)
            layout.addWidget(label, 0, i * 2, 1, 2)

            # 🔹 garante que cada coluna tenha o mesmo peso do grid
            layout.setColumnStretch(i * 2, 1)
            layout.setColumnStretch(i * 2 + 1, 1)
