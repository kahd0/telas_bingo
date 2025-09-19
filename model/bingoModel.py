from PySide6.QtCore import QObject, Signal

class BingoModel(QObject):
    stoneSelected = Signal(int)
    stoneUnselected = Signal(int)
    resetDone = Signal()

    def __init__(self):
        super().__init__()
        self.stones = {i: {"selected": False, "wasUnselected": False} for i in range(1, 101)}
        self.lastStones = []

    def selectStone(self, number):
        if not self.stones[number]["selected"]:
            self.stones[number]["selected"] = True
            self.stones[number]["wasUnselected"] = False
            self.lastStones.append(number)
            if len(self.lastStones) > 10:
                self.lastStones.pop(0)
            self.stoneSelected.emit(number)

    def unselectStone(self, number):
        if self.stones[number]["selected"]:
            self.stones[number]["selected"] = False
            self.stones[number]["wasUnselected"] = True
            self.stoneUnselected.emit(number)

    def resetAll(self):
        for k in self.stones:
            self.stones[k] = {"selected": False, "wasUnselected": False}
        self.lastStones.clear()
        self.resetDone.emit()

    def getColumnLetter(self, number):
        col = (number - 1) // 10
        if number == 100:
            col = 9
        if col in [0, 1]:
            return "B"
        if col in [2, 3]:
            return "I"
        if col in [4, 5]:
            return "N"
        if col in [6, 7]:
            return "G"
        return "O"
