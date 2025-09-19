import sys
from typing import NoReturn  # Add for type hinting
from PySide6.QtWidgets import QApplication
from model.bingoModel import BingoModel
from ui.operatorWindow import OperatorWindow
from ui.publicWindow import PublicWindow


def main() -> NoReturn:
    app = QApplication(sys.argv)
    model = BingoModel()

    # cria a tela pública primeiro
    publicWindow = PublicWindow(model)

    # passa a instância da tela pública para a tela do operador
    operatorWindow = OperatorWindow(model, publicWindow=publicWindow)

    # conecta os sinais do modelo à tela pública
    model.stoneSelected.connect(publicWindow.showStone)
    model.stoneUnselected.connect(publicWindow.unshowStone)
    model.resetDone.connect(publicWindow.resetView)

    operatorWindow.showMaximized()
    publicWindow.showFullScreen()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application exited with error: {e}")


if __name__ == "__main__":
    main()
