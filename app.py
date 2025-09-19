import sys
from PySide6.QtWidgets import QApplication
from model.bingoModel import BingoModel
from ui.operatorWindow import OperatorWindow
from ui.publicWindow import PublicWindow

def main():
    app = QApplication(sys.argv)
    model = BingoModel()
    operatorWindow = OperatorWindow(model)
    publicWindow = PublicWindow(model)
    model.stoneSelected.connect(publicWindow.showStone)
    model.stoneUnselected.connect(publicWindow.unshowStone)
    model.resetDone.connect(publicWindow.resetView)
    operatorWindow.showMaximized()
    publicWindow.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
