from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QMovie

import main
import mainwindow
import wifi_settings
import mail_settings
import receivers_list
import datetime
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
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] FSM Thread Running")
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
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 将WiFi连接功能设置为 {param}")
        FSMMutex.unlock()

    def set_enable_wifi_reconnect(self, param):
        FSMMutex.lock()
        self.FSM.set_enable_wifi_reconnect(param)
        self.SIGNAL_enable_wifi_reconnect.emit()
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 将失败重连功能设置为 {param}")
        FSMMutex.unlock()

    def set_enable_mail_notification(self, param):
        FSMMutex.lock()
        self.FSM.set_enable_mail_notification(param)
        self.SIGNAL_enable_mail_notification.emit()
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 将邮件通知功能设置为 {param}")
        FSMMutex.unlock()

    def get_enable_wifi_connect(self):
        return self.FSM.enable_wifi_connect

    def get_enable_wifi_reconnect(self):
        return self.FSM.enable_wifi_reconnect

    def get_enable_mail_notification(self):
        return self.FSM.enable_mail_notification

    def get_mail_config(self):
        return self.FSM.config["mail_config"]


class stdoutRedirect:
    def __init__(self, textBrowser):
        self.textBrowser = textBrowser

    def write(self, string):
        self.textBrowser.moveCursor(QTextCursor.MoveOperation.End)
        self.textBrowser.insertPlainText(string)

    def flush(self):
        pass


class receiversDialog(QtWidgets.QDialog):
    SIGNAL_delete_item = QtCore.pyqtSignal()

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == Qt.Key.Key_Delete:
            self.SIGNAL_delete_item.emit()


def set_wifi_account(FSM_d: FSM_Thread):
    dialog = QtWidgets.QDialog()
    dialog_ui = wifi_settings.Ui_Dialog()
    dialog_ui.setupUi(dialog)
    cur_wifi_config = FSM_d.FSM.get_wifi_config()
    dialog_ui.lineEdit_1.setText(cur_wifi_config["username"])
    dialog_ui.lineEdit_2.setText(cur_wifi_config["password"])
    if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 已设置WiFi账号密码")
        FSMMutex.lock()
        FSM_d.FSM.set_wifi_account(dialog_ui.lineEdit_1.text(), dialog_ui.lineEdit_2.text())
        FSMMutex.unlock()


def set_mail_account(FSM_d: FSM_Thread):
    dialog = QtWidgets.QDialog()
    dialog_ui = mail_settings.Ui_Dialog()
    dialog_ui.setupUi(dialog)
    cur_mail_config = FSM_d.get_mail_config()
    dialog_ui.mail_account.setText(cur_mail_config["mail_user"])
    dialog_ui.mail_password.setText(cur_mail_config["mail_pass"])
    dialog_ui.SMTP_host.setText(cur_mail_config["mail_host"])
    dialog_ui.SMTP_port.setText(str(cur_mail_config["mail_port"]))
    dialog_ui.pushButton.clicked.connect(lambda: set_receivers(FSM_d))
    if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 已配置邮件")
        FSMMutex.lock()
        FSM_d.FSM.set_mail_account(dialog_ui.mail_account.text(), dialog_ui.mail_password.text())
        FSM_d.FSM.set_mail_smtp(dialog_ui.SMTP_host.text(), dialog_ui.SMTP_port.text())
        FSMMutex.unlock()


def set_receivers(FSM_d: FSM_Thread):
    dialog = receiversDialog()
    dialog_ui = receivers_list.Ui_Dialog()
    dialog_ui.setupUi(dialog)
    dialog_ui.confirmButton.clicked.connect(lambda: dialog.accept())
    cur_mail_config = FSM_d.get_mail_config()
    dialog_ui.listWidget.addItems(cur_mail_config["receivers"])

    def delete_item():
        selected_items = dialog_ui.listWidget.selectedItems()
        for item in selected_items:
            dialog_ui.listWidget.takeItem(dialog_ui.listWidget.row(item))

    def add_item():
        if len(dialog_ui.lineEdit.text()):
            dialog_ui.listWidget.addItem(dialog_ui.lineEdit.text())
            dialog_ui.lineEdit.clear()

    dialog_ui.deleteButton.clicked.connect(lambda: delete_item())
    dialog.SIGNAL_delete_item.connect(lambda: delete_item())
    dialog_ui.addButton.clicked.connect(lambda: add_item())

    if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 已配置收件人列表")
        FSMMutex.lock()
        FSM_d.FSM.set_receivers([dialog_ui.listWidget.item(i).text() for i in range(dialog_ui.listWidget.count())])
        FSMMutex.unlock()


tag = 0
if main.check_first_run():
    tag = 1
FSM_t = FSM_Thread()
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
MainWindow.setWindowIcon(QtGui.QIcon("favicon.ico"))
ui = mainwindow.Ui_MainWindow()
ui.setupUi(MainWindow)

FSM_t.load_state()
FSM_t.taskFinished.connect(lambda: FSM_t.load_state())
sys.stdout = stdoutRedirect(ui.textBrowser)
timer = QtCore.QTimer()
timer.timeout.connect(lambda: FSM_t.start())
timer.setInterval(20000)

movie = QMovie("AL1S.gif")
ui.MovieLabel_1.setMovie(movie)
ui.MovieLabel_2.setMovie(movie)
ui.MovieLabel_1.setScaledContents(True)
ui.MovieLabel_2.setScaledContents(True)
movie.start()

ui.tabWidget.setCurrentWidget(ui.generalTab)
ui.checkBox_1.stateChanged.connect(lambda: FSM_t.set_enable_wifi_connect(ui.checkBox_1.isChecked()))
ui.checkBox_2.stateChanged.connect(lambda: FSM_t.set_enable_wifi_reconnect(ui.checkBox_2.isChecked()))
ui.checkBox_3.stateChanged.connect(lambda: FSM_t.set_enable_mail_notification(ui.checkBox_3.isChecked()))
ui.textBrowser.textChanged.connect(lambda: ui.textBrowser.moveCursor(QTextCursor.MoveOperation.End))
ui.pushButton_1.clicked.connect(lambda: set_wifi_account(FSM_t))
ui.pushButton_2.clicked.connect(lambda: set_mail_account(FSM_t))
FSM_t.SIGNAL_enable_wifi_connect.connect(
    lambda: ui.checkBox_1.setText("已启用" if FSM_t.get_enable_wifi_connect() else "未启用"))
FSM_t.SIGNAL_enable_wifi_reconnect.connect(
    lambda: ui.checkBox_2.setText("已启用" if FSM_t.get_enable_wifi_reconnect() else "未启用"))
FSM_t.SIGNAL_enable_mail_notification.connect(
    lambda: ui.checkBox_3.setText("已启用" if FSM_t.get_enable_mail_notification() else "未启用"))

if tag == 0:
    QMessageBox = QtWidgets.QMessageBox()
    QMessageBox.setWindowTitle("欢迎使用BUPT-Network-Control-Panel！")
    QMessageBox.setText("首次运行，请先配置WiFi账号密码和邮件账号密码")
    QMessageBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    QMessageBox.exec()
    ui.tabWidget.setCurrentWidget(ui.SettingTab)
    set_wifi_account(FSM_t)
    set_mail_account(FSM_t)

MainWindow.show()
timer.start()
sys.exit(app.exec())
