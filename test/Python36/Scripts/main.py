import sys
from PyQt5 import QtWidgets
import os

import design

class ExampleApp (QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ButtonBrowse.clicked.connect(self.browse_folder)
        self.ButtonExit.clicked.connect(self.clear_list)

    def browse_folder(self):
        self.listWidget.clear() #Отчищаем список, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)

    def clear_list(self):
        self.listWidget.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()       #создаем объект класса ExampleApp
    window.show()               #показываем окно
    app.exec_()                 #запускаем приложение

#Если запускаем файл напрямую, а не импортируем, то запускаем функцию main()
if __name__ == "__main__":
    main()