# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.splitter_vertical = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter_vertical.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter_vertical.setObjectName("splitter_vertical")
        self.tableWidgetWrapper = QtWidgets.QWidget(parent=self.splitter_vertical)
        self.tableWidgetWrapper.setObjectName("tableWidgetWrapper")
        self.tableLayout = QtWidgets.QVBoxLayout(self.tableWidgetWrapper)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setObjectName("tableLayout")
        self.fileLabel = QtWidgets.QLabel(parent=self.tableWidgetWrapper)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(12)
        font.setBold(True)
        self.fileLabel.setFont(font)
        self.fileLabel.setObjectName("fileLabel")
        self.tableLayout.addWidget(self.fileLabel)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.tableWidgetWrapper)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableLayout.addWidget(self.tableWidget)
        self.splitterWrapper = QtWidgets.QWidget(parent=self.splitter_vertical)
        self.splitterWrapper.setObjectName("splitterWrapper")
        self.splitterLayout = QtWidgets.QVBoxLayout(self.splitterWrapper)
        self.splitterLayout.setContentsMargins(0, 0, 0, 0)
        self.splitterLayout.setObjectName("splitterLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.splitterWrapper)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.leftWidget = QtWidgets.QWidget(parent=self.splitter)
        self.leftWidget.setObjectName("leftWidget")
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setObjectName("leftLayout")
        self.sceneLabel = QtWidgets.QLabel(parent=self.leftWidget)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(12)
        font.setBold(True)
        self.sceneLabel.setFont(font)
        self.sceneLabel.setObjectName("sceneLabel")
        self.leftLayout.addWidget(self.sceneLabel)
        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.leftWidget)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tableWidget_2.setRowCount(3)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        self.leftLayout.addWidget(self.tableWidget_2)
        self.rightWidget = QtWidgets.QWidget(parent=self.splitter)
        self.rightWidget.setObjectName("rightWidget")
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightWidget)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setObjectName("rightLayout")
        self.sceneLabel_2 = QtWidgets.QLabel(parent=self.rightWidget)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(12)
        font.setBold(True)
        self.sceneLabel_2.setFont(font)
        self.sceneLabel_2.setObjectName("sceneLabel_2")
        self.rightLayout.addWidget(self.sceneLabel_2)
        self.logTextEdit = QtWidgets.QTextEdit(parent=self.rightWidget)
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        self.logTextEdit.setFont(font)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.rightLayout.addWidget(self.logTextEdit)
        self.progressBar = QtWidgets.QProgressBar(parent=self.rightWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.rightLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(parent=self.rightWidget)
        self.pushButton.setObjectName("pushButton")
        self.rightLayout.addWidget(self.pushButton)
        self.splitterLayout.addWidget(self.splitter)
        self.verticalLayout.addWidget(self.splitter_vertical)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtGui.QAction(parent=MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_generate_report = QtGui.QAction(parent=MainWindow)
        self.action_generate_report.setObjectName("action_generate_report")
        self.menu.addAction(self.action_open)
        self.menu_2.addAction(self.action_generate_report)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "导航数据处理"))
        self.titleLabel.setText(_translate("MainWindow", "导航数据处理"))
        self.fileLabel.setText(_translate("MainWindow", "文件信息"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "文件名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "文件格式"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "频率"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "真值文件"))
        self.sceneLabel.setText(_translate("MainWindow", "场景信息"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "场景"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "开始时间"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "结束时间"))
        self.sceneLabel_2.setText(_translate("MainWindow", "日志输出"))
        self.logTextEdit.setPlaceholderText(_translate("MainWindow", "日志输出..."))
        self.pushButton.setText(_translate("MainWindow", "计算误差"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "报告"))
        self.action_open.setText(_translate("MainWindow", "打开数据"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_generate_report.setText(_translate("MainWindow", "生成报告"))
        self.action_generate_report.setShortcut(_translate("MainWindow", "Ctrl+R"))
