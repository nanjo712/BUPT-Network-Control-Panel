# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 331)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 601, 301))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.NetStateDisplay = QtWidgets.QLabel(parent=self.generalTab)
        self.NetStateDisplay.setGeometry(QtCore.QRect(130, 50, 71, 21))
        self.NetStateDisplay.setObjectName("NetStateDisplay")
        self.SSIDLabel = QtWidgets.QLabel(parent=self.generalTab)
        self.SSIDLabel.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.SSIDLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.SSIDLabel.setObjectName("SSIDLabel")
        self.IPDisplay = QtWidgets.QLabel(parent=self.generalTab)
        self.IPDisplay.setGeometry(QtCore.QRect(130, 80, 71, 16))
        self.IPDisplay.setObjectName("IPDisplay")
        self.SSIDDisplay = QtWidgets.QLabel(parent=self.generalTab)
        self.SSIDDisplay.setGeometry(QtCore.QRect(130, 26, 71, 20))
        self.SSIDDisplay.setObjectName("SSIDDisplay")
        self.IPLabel = QtWidgets.QLabel(parent=self.generalTab)
        self.IPLabel.setGeometry(QtCore.QRect(30, 80, 81, 16))
        self.IPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.IPLabel.setObjectName("IPLabel")
        self.NetStateLabel = QtWidgets.QLabel(parent=self.generalTab)
        self.NetStateLabel.setGeometry(QtCore.QRect(30, 50, 81, 21))
        self.NetStateLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.NetStateLabel.setObjectName("NetStateLabel")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.generalTab)
        self.textBrowser.setGeometry(QtCore.QRect(230, 10, 351, 251))
        self.textBrowser.setStyleSheet("")
        self.textBrowser.setObjectName("textBrowser")
        self.MovieLabel_1 = QtWidgets.QLabel(parent=self.generalTab)
        self.MovieLabel_1.setGeometry(QtCore.QRect(40, 120, 161, 141))
        self.MovieLabel_1.setObjectName("MovieLabel_1")
        self.tabWidget.addTab(self.generalTab, "")
        self.SettingTab = QtWidgets.QWidget()
        self.SettingTab.setObjectName("SettingTab")
        self.label_3 = QtWidgets.QLabel(parent=self.SettingTab)
        self.label_3.setGeometry(QtCore.QRect(50, 50, 61, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.checkBox_3 = QtWidgets.QCheckBox(parent=self.SettingTab)
        self.checkBox_3.setGeometry(QtCore.QRect(140, 80, 81, 31))
        self.checkBox_3.setObjectName("checkBox_3")
        self.label_1 = QtWidgets.QLabel(parent=self.SettingTab)
        self.label_1.setGeometry(QtCore.QRect(40, 80, 71, 31))
        self.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(parent=self.SettingTab)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 91, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.SettingTab)
        self.checkBox_2.setGeometry(QtCore.QRect(140, 50, 81, 31))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_1 = QtWidgets.QCheckBox(parent=self.SettingTab)
        self.checkBox_1.setGeometry(QtCore.QRect(140, 20, 81, 31))
        self.checkBox_1.setObjectName("checkBox_1")
        self.label_5 = QtWidgets.QLabel(parent=self.SettingTab)
        self.label_5.setGeometry(QtCore.QRect(310, 170, 61, 31))
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.SettingTab)
        self.label_6.setGeometry(QtCore.QRect(280, 20, 91, 31))
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton_1 = QtWidgets.QPushButton(parent=self.SettingTab)
        self.pushButton_1.setGeometry(QtCore.QRect(390, 20, 191, 31))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.SettingTab)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 170, 191, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.MovieLabel_2 = QtWidgets.QLabel(parent=self.SettingTab)
        self.MovieLabel_2.setGeometry(QtCore.QRect(40, 120, 161, 141))
        self.MovieLabel_2.setObjectName("MovieLabel_2")
        self.tabWidget.addTab(self.SettingTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label_3.setBuddy(self.checkBox_2)
        self.label_1.setBuddy(self.checkBox_3)
        self.label_2.setBuddy(self.checkBox_1)
        self.label_5.setBuddy(self.pushButton_2)
        self.label_6.setBuddy(self.pushButton_1)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.textBrowser, self.checkBox_1)
        MainWindow.setTabOrder(self.checkBox_1, self.checkBox_2)
        MainWindow.setTabOrder(self.checkBox_2, self.checkBox_3)
        MainWindow.setTabOrder(self.checkBox_3, self.pushButton_1)
        MainWindow.setTabOrder(self.pushButton_1, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.tabWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "北邮校园网控制面板"))
        self.NetStateDisplay.setText(_translate("MainWindow", "Waiting"))
        self.SSIDLabel.setText(_translate("MainWindow", "当前WiFi_SSID"))
        self.IPDisplay.setText(_translate("MainWindow", "Waiting"))
        self.SSIDDisplay.setText(_translate("MainWindow", "Waiting"))
        self.IPLabel.setText(_translate("MainWindow", "当前IP地址"))
        self.NetStateLabel.setText(_translate("MainWindow", "当前网络状态"))
        self.MovieLabel_1.setText(_translate("MainWindow", "MovieLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("MainWindow", "总览"))
        self.label_3.setText(_translate("MainWindow", "失败重连"))
        self.checkBox_3.setText(_translate("MainWindow", "未启用"))
        self.label_1.setText(_translate("MainWindow", "邮件通知"))
        self.label_2.setText(_translate("MainWindow", "WiFi自动连接"))
        self.checkBox_2.setText(_translate("MainWindow", "未启用"))
        self.checkBox_1.setText(_translate("MainWindow", "未启用"))
        self.label_5.setText(_translate("MainWindow", "邮件设置"))
        self.label_6.setText(_translate("MainWindow", "WiFi账号设置"))
        self.pushButton_1.setText(_translate("MainWindow", "Go"))
        self.pushButton_2.setText(_translate("MainWindow", "Go"))
        self.MovieLabel_2.setText(_translate("MainWindow", "MovieLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SettingTab), _translate("MainWindow", "设置"))
