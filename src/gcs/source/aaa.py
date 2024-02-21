from PyQt5 import QtWidgets









class CentralWidget(QtWidgets.QWidget):
	def __init__(self):
		super(CentralWidget, self).__init__()
		self.textEdit = QtWidgets.QTextEdit()
		self.button = QtWidgets.QPushButton()
		self.layoutube = QtWidgets.QHBoxLayout()
		self.setLayout(self.layoutube)
		self.layoutube.addWidget(self.textEdit)
		self.layoutube2 = QtWidgets.QVBoxLayout()
		self.layoutube.addLayout(self.layoutube2)
		self.layoutube.addWidget(self.textEdit)

		self.layoutube2.addWidget(self.textEdit)
		self.layoutube2.addWidget(self.textEdit)



class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("ROMA GA Y")
		self.resize(1488, 322)
		self.move_center()
		self.c_widget = CentralWidget();
		self.setCentralWidget(self.c_widget) 


	def move_center(self):
		frame = self.frameGeometry()
		frame.moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())
		self.move(frame.topLeft())