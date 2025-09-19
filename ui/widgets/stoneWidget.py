from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PySide6.QtCore import Qt, Signal

class StoneWidget(QPushButton):
    clicked = Signal()

    def __init__(self, number, publicView=False):
        super().__init__()
        self.number = number
        self.publicView = publicView
        self.selected = False
        self.wasUnselected = False
        self.setMinimumSize(70, 70)

    def emitClicked(self):
        if not self.publicView:
            self.clicked.emit()

    def displayNumber(self):
        return f"{self.number if self.number < 100 else '00'}"

    def paintEvent(self, event):
        diameter = min(self.width(), self.height())
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()

        # 🔹 Define as cores
        if self.publicView:
            color = QColor("#FFFFFF")  # Sempre branco para o público
            textColor = QColor("#000000")
        else:
            if self.selected:
                color = QColor("#2D7BE1")
                textColor = QColor("#FFFFFF")
            elif self.wasUnselected:
                color = QColor("#FFFFFF")
                textColor = QColor("#D7263D")
            else:
                color = QColor("#FFFFFF")
                textColor = QColor("#000000")

        qp.setBrush(QBrush(color))
        qp.setPen(QPen(Qt.black, 2))
        qp.drawEllipse(center, diameter // 2 - 5, diameter // 2 - 5)

        # 🔹 Fonte proporcional ao tamanho do círculo
        font = qp.font()
        font.setPointSize(int(diameter * 0.45))  # quase ocupando o círculo
        font.setBold(True)
        qp.setFont(font)

        qp.setPen(textColor)
        qp.drawText(rect, Qt.AlignCenter, self.displayNumber())

    def setSelected(self, value, wasUnselected=False):
        self.selected = value
        self.wasUnselected = wasUnselected
        self.update()

    def reset(self):
        self.selected = False
        self.wasUnselected = False
        self.update()
