from typing import Optional  # Add for type hinting
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QApplication,
)
from PySide6.QtCore import Qt
from ui.widgets.stoneWidget import StoneWidget
from ui.widgets.headerWidget import HeaderWidget


class PublicWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f8f9fa, stop: 1 #e9ecef);
            }
            QWidget {
                background-color: transparent;
                color: #2c3e50;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
        )
        self.setWindowTitle("🎯 Bingo da Igreja - Painel Público")
        self.model = model

        central = QWidget()
        central.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 0.5 #f8f9fa, stop: 1 #e9ecef);
                border-radius: 15px;
                margin: 10px;
            }
        """
        )
        layout = QHBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # 🔹 Grade de pedras
        gridContainer = QWidget()
        gridContainer.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 1 #f8f9fa);
                border: 3px solid #3498db;
                border-radius: 20px;
                padding: 15px;
            }
        """
        )
        gridLayout = QVBoxLayout(gridContainer)
        gridLayout.setContentsMargins(15, 15, 15, 15)
        gridLayout.setSpacing(10)

        self.header = HeaderWidget()
        gridLayout.addWidget(self.header)

        # Container para a grade com sombra
        gridWidget = QWidget()
        gridWidget.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 15px;
                padding: 10px;
            }
        """
        )
        gridWidgetLayout = QVBoxLayout(gridWidget)
        gridWidgetLayout.setContentsMargins(10, 10, 10, 10)

        self.grid = QGridLayout()
        self.grid.setSpacing(3)  # espaçamento entre pedras

        # 🔹 garante largura uniforme das 10 colunas
        for col in range(10):
            self.grid.setColumnStretch(col, 1)

        self.stoneWidgets: dict[int, StoneWidget] = {}
        for col in range(10):
            for row in range(10):
                number = col * 10 + row + 1
                if number == 100:
                    number = 100
                stone = StoneWidget(number, publicView=True)
                stone.setVisible(False)
                self.grid.addWidget(stone, row, col)
                self.stoneWidgets[number] = stone

        gridWidgetLayout.addLayout(self.grid)
        gridLayout.addWidget(gridWidget)

        # 🔹 empurra o grid um pouco para cima
        gridLayout.addSpacerItem(
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        layout.addWidget(gridContainer)

        # 🔹 Caixa lateral de últimas pedras
        self.lastColumn = QWidget()
        self.lastColumn.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 1 #f1c40f);
                border: 3px solid #f39c12;
                border-radius: 20px;
                padding: 20px;
            }
        """
        )
        self.lastColumnLayout = QVBoxLayout(self.lastColumn)
        self.lastColumnLayout.setAlignment(Qt.AlignTop)
        self.lastColumnLayout.setContentsMargins(15, 15, 15, 15)
        self.lastColumnLayout.setSpacing(15)

        # Título da seção
        titleLabel = QLabel("🎲 ÚLTIMAS PEDRAS")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #8b4513;
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid #d4aa00;
                border-radius: 10px;
                padding: 8px;
                margin-bottom: 10px;
            }
        """
        )
        self.lastColumnLayout.addWidget(titleLabel)

        self.lastStoneLabels = []
        for i in range(5):  # até 5 últimas pedras
            lbl = QLabel("")
            lbl.setAlignment(Qt.AlignCenter)
            if i == 0:  # primeira pedra (mais recente)
                lbl.setStyleSheet(
                    """
                    QLabel {
                        font-size: 120px;
                        font-weight: bold;
                        color: #c0392b;
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #ffffff, stop: 1 #ecf0f1);
                        border: 4px solid #e74c3c;
                        border-radius: 15px;
                        padding: 15px;
                        margin: 5px;
                    }
                """
                )
            else:
                lbl.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {80 - i*10}px;
                        font-weight: bold;
                        color: #2c3e50;
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 #ffffff, stop: 1 #bdc3c7);
                        border: 2px solid #95a5a6;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 3px;
                        opacity: {1.0 - i*0.15};
                    }}
                """
                )
            self.lastColumnLayout.addWidget(lbl)
            self.lastStoneLabels.append(lbl)

        # Espaçador para empurrar tudo para cima
        self.lastColumnLayout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        layout.addWidget(self.lastColumn)

        self.setCentralWidget(central)

        # Define tamanho mínimo da janela
        self.setMinimumSize(1200, 800)

        # 🖥️ Configuração para múltiplas telas (projetor)
        self.setupProjectorDisplay()

    def showStone(self, number: int):
        stone = self.stoneWidgets.get(number)
        if stone:
            stone.setVisible(True)
            stone.setSelected(True)
            self.updateLastList()

    def unshowStone(self, number: int):
        stone = self.stoneWidgets.get(number)
        if stone:
            stone.setVisible(True)
            stone.setSelected(False, wasUnselected=True)
            self.updateLastList()

    def resetView(self):
        for stone in self.stoneWidgets.values():
            stone.reset()
            stone.setVisible(False)
        for lbl in self.lastStoneLabels:
            lbl.clear()

    def updateLastList(self):
        # Atualiza labels (última pedra no topo, destaque maior)
        stones = self.model.lastStones[::-1]  # inverte ordem
        for i, lbl in enumerate(self.lastStoneLabels):
            if i < len(stones):
                num = stones[i]
                displayNum = "00" if num == 100 else str(num)
                lbl.setText(f"{self.model.getColumnLetter(num)}-{displayNum}")
            else:
                lbl.clear()

    def setupProjectorDisplay(self):
        """Configura a janela para exibição em projetor se disponível"""
        screens = QApplication.screens()
        if len(screens) > 1:
            # se houver mais de uma tela, assume que a segunda é o projetor
            projectorScreen = screens[1]
            geometry = projectorScreen.availableGeometry()
            # move e redimensiona para ocupar toda a tela do projetor
            self.setGeometry(geometry)
            self.move(geometry.x(), geometry.y())
            self.showMaximized()
        else:
            # se não houver projetor, apenas maximiza na tela atual
            self.showMaximized()
