from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, 
    QMessageBox, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont
import os
from ui.widgets.stoneWidget import StoneWidget
from ui.widgets.headerWidget import HeaderWidget
from utils.phoneLink import openWhatsappLink


class OperatorWindow(QMainWindow):
    def __init__(self, model, publicWindow=None):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join("assets", "logo.ico")))
        self.setWindowTitle("🎯 Bingo da Igreja - Painel do Operador")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: transparent;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        self.model = model
        self.publicWindow = publicWindow   # mantém referência para a tela do público
        central = QWidget()
        central.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 5px;
            }
        """)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header simples
        self.header = HeaderWidget()
        layout.addWidget(self.header)

        # Grade de pedras simples
        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        
        # Garante largura uniforme das colunas
        for col in range(10):
            self.grid.setColumnStretch(col, 1)

        self.stoneWidgets = {}
        for col in range(10):
            for row in range(10):
                number = col * 10 + row + 1
                if number == 100:
                    number = 100  # mantém "00" como último
                stone = StoneWidget(number)
                stone.clicked.connect(lambda checked=False, num=number: self.handleClick(num))
                self.grid.addWidget(stone, row, col)
                self.stoneWidgets[number] = stone

        layout.addLayout(self.grid)

        # Footer simples
        footer = QHBoxLayout()
        
        # Botão de reiniciar simples
        resetBtn = QPushButton("🔄 Reiniciar")
        resetBtn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #e74c3c;
                border: 2px solid #c0392b;
                border-radius: 6px;
                padding: 10px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
        """)
        resetBtn.clicked.connect(self.resetGame)
        
        footer.addStretch()
        footer.addWidget(resetBtn)
        footer.addWidget(self.createFooterLabel())
        

        # Botão Encerrar
        exitBtn = QPushButton("❌ Encerrar")
        exitBtn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #7f8c8d;
                border: 2px solid #626e70;
                border-radius: 6px;
                padding: 10px 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
            QPushButton:pressed {
                background-color: #626e70;
            }
        """)
        exitBtn.clicked.connect(QApplication.quit)

        # Botão Tela do Público
        publicBtn = QPushButton("🖥️ Tela do Público")
        publicBtn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #27ae60;
                border: 2px solid #1e8449;
                border-radius: 6px;
                padding: 10px 20px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        publicBtn.clicked.connect(self.openPublicWindow)

        # Botão Reiniciar (já existia)
        resetBtn = QPushButton("🔄 Reiniciar")
        resetBtn.setStyleSheet(""" ... """)  # mantém seu estilo
        resetBtn.clicked.connect(self.resetGame)

        footer.addStretch()
        footer.addWidget(exitBtn)
        footer.addWidget(publicBtn)
        footer.addWidget(resetBtn)
        footer.addWidget(self.createFooterLabel())
        
        layout.addLayout(footer)

        self.setCentralWidget(central)
        
        # Define tamanho mínimo
        self.setMinimumSize(900, 650)
        
        # Conecta os sinais
        self.model.stoneSelected.connect(self.updateStone)
        self.model.stoneUnselected.connect(self.updateStoneUnselected)
        self.model.resetDone.connect(self.resetView)

    def createFooterLabel(self):
        label = QLabel('<a href="https://wa.me/5548998160074" style="color: #3498db; text-decoration: none;">📱 Desenvolvido por Ricardo Vieira (48) 99816-0074</a>')
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #666;
                padding: 5px;
            }
        """)
        return label

    def handleClick(self, number):
        stone = self.stoneWidgets[number]
        if self.model.stones[number]["selected"]:
            # Dialog de confirmação melhorado
            reply = self.showStyledMessageBox(
                "⚠️ Confirmação", 
                f"Deseja desmarcar a pedra {stone.displayNumber()}?",
                QMessageBox.Question
            )
            if reply == QMessageBox.Yes:
                self.model.unselectStone(number)
        else:
            self.model.selectStone(number)

    def resetGame(self):
        reply = self.showStyledMessageBox(
            "🔄 Reiniciar Jogo", 
            "Deseja desmarcar todas as pedras e iniciar uma nova partida?",
            QMessageBox.Question
        )
        if reply == QMessageBox.Yes:
            self.model.resetAll()

    def showStyledMessageBox(self, title, message, icon):
        """Cria um MessageBox simples"""
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setIcon(icon)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msgBox.exec_()

    def updateStone(self, number):
        self.stoneWidgets[number].setSelected(True)

    def updateStoneUnselected(self, number):
        self.stoneWidgets[number].setSelected(False, wasUnselected=True)

    def resetView(self):
        for stone in self.stoneWidgets.values():
            stone.reset()

    def openPublicWindow(self):
        if self.publicWindow is not None:
            self.publicWindow.show()
            self.publicWindow.raise_()
            self.publicWindow.activateWindow()
        else:
            QMessageBox.information(
                self, "Tela do Público", 
                "A tela do público não foi inicializada nesta sessão."
            )