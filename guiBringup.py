import main
import mainwindow
from PyQt6 import QtCore, QtGui, QtWidgets
import sys

FSMMutex = QtCore.QMutex()


class FSM_Thread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    SIGNAL_enable_wifi_connect = QtCore.pyqtSignal()
    SIGNAL_enable_wifi_reconnect = QtCore.pyqtSignal()
    SIGNAL_enable_mail_notification = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.FSM = main.AUTOFSM()

    def run(self):
        FSMMutex.lock()
        self.FSM.run()
        self.taskFinished.emit()
        FSMMutex.unlock()

    def load_state(self):
        FSMMutex.lock()
        ui.SSIDDisplay.setText(
            self.FSM.get_current_wifi_ssid() if self.FSM.get_current_wifi_ssid() is not None else "未知")
        ui.NetStateDisplay.setText("已连接" if self.FSM.check_wifi_state() else "未连接")
        ui.IPDisplay.setText(self.FSM.get_ip_address())
        ui.checkBox_1.setChecked(self.FSM.enable_wifi_connect)
        ui.checkBox_2.setChecked(self.FSM.enable_wifi_reconnect)
        ui.checkBox_3.setChecked(self.FSM.enable_mail_notification)
        ui.checkBox_1.setText("已启用" if self.FSM.enable_wifi_connect else "未启用")
        ui.checkBox_2.setText("已启用" if self.FSM.enable_wifi_reconnect else "未启用")
        ui.checkBox_3.setText("已启用" if self.FSM.enable_mail_notification else "未启用")
        FSMMutex.unlock()

    def set_enable_wifi_connect(self, param):
        FSMMutex.lock()
        self.FSM.set_enable_wifi_connect(param)
        self.SIGNAL_enable_wifi_connect.emit()
        FSMMutex.unlock()

    def set_enable_wifi_reconnect(self, param):
        FSMMutex.lock()
        self.FSM.set_enable_wifi_reconnect(param)
        self.SIGNAL_enable_wifi_reconnect.emit()
        FSMMutex.unlock()

    def set_enable_mail_notification(self, param):
        FSMMutex.lock()
        self.FSM.set_enable_mail_notification(param)
        self.SIGNAL_enable_mail_notification.emit()
        FSMMutex.unlock()

    def get_enable_wifi_connect(self):
        return self.FSM.enable_wifi_connect

    def get_enable_wifi_reconnect(self):
        return self.FSM.enable_wifi_reconnect

    def get_enable_mail_notification(self):
        return self.FSM.enable_mail_notification


FSM_t = FSM_Thread()
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow)
FSM_t.load_state()
timer = QtCore.QTimer()
timer.timeout.connect(lambda: FSM_t.start())
timer.setInterval(20000)
FSM_t.taskFinished.connect(lambda: FSM_t.load_state())
timer.start()

ui.tabWidget.setCurrentWidget(ui.generalTab)
ui.checkBox_1.stateChanged.connect(lambda: FSM_t.set_enable_wifi_connect(ui.checkBox_1.isChecked()))
ui.checkBox_2.stateChanged.connect(lambda: FSM_t.set_enable_wifi_reconnect(ui.checkBox_2.isChecked()))
ui.checkBox_3.stateChanged.connect(lambda: FSM_t.set_enable_mail_notification(ui.checkBox_3.isChecked()))
FSM_t.SIGNAL_enable_wifi_connect.connect(
    lambda: ui.checkBox_1.setText("已启用" if FSM_t.get_enable_wifi_connect() else "未启用"))
FSM_t.SIGNAL_enable_wifi_reconnect.connect(
    lambda: ui.checkBox_2.setText("已启用" if FSM_t.get_enable_wifi_reconnect() else "未启用"))
FSM_t.SIGNAL_enable_mail_notification.connect(
    lambda: ui.checkBox_3.setText("已启用" if FSM_t.get_enable_mail_notification() else "未启用"))


MainWindow.show()
sys.exit(app.exec())
