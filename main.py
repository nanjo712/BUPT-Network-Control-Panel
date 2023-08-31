import yaml_process
import pywifi
import socket
import smtplib
import time
import requests
import subprocess
import os
import sys
import netifaces
import datetime
from email.mime.text import MIMEText
from email.header import Header
import urllib.request
import urllib.error

current_os = sys.platform


def check_internet_connection():
    try:
        urllib.request.urlopen('https://www.baidu.com', timeout=1)
        return True
    except urllib.error.URLError:
        return False


class AUTOFSM:
    def __init__(self):
        self.data = yaml_process.read_data()
        self.config = yaml_process.read_config()
        self.enable_mail_notification = self.config["enable_mail_notification"]
        self.enable_wifi_connect = self.config["enable_wifi_connect"]
        self.enable_wifi_reconnect = self.config["enable_wifi_reconnect"]
        self.username = self.config["wifi_config"]["username"]
        self.password = self.config["wifi_config"]["password"]
        self.url = self.data["url"]
        self.last_host_name = self.data["last_host_name"]
        self.last_ip_address = self.data["last_ip_address"]
        self.network_ssid = self.data["portal_SSID"]
        self.max_wait_time = self.config["max_wait_time"]
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def get_ip_address(self):
        if current_os == "win32":
            return socket.gethostbyname(socket.gethostname())
        elif current_os == "linux":
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addresses:
                    for address in addresses[netifaces.AF_INET]:
                        ip = address['addr']
                        if ip != '127.0.0.1':
                            return ip
        return None

    def check_ip(self):
        hostname = socket.gethostname()
        ip_address = self.get_ip_address()
        if (hostname is None) or (ip_address is None): return False
        if (hostname != self.last_host_name) or (ip_address != self.last_ip_address):
            self.data["last_host_name"] = hostname
            self.data["last_ip_address"] = ip_address
            self.last_host_name = hostname
            self.last_ip_address = ip_address
            yaml_process.write_data(self.data)
            return True
        else:
            return False

    def mail_notification(self, hostname, ip_address):
        mail_config = self.config["mail_config"]
        mail_host = mail_config["mail_host"]
        mail_port = mail_config["mail_port"]
        mail_user = mail_config["mail_user"]
        mail_pass = mail_config["mail_pass"]
        sender = mail_config["sender"]
        receivers = mail_config["receivers"]

        message = MIMEText(f"IP地址或主机名发生变化，新的主机名为{hostname}，新的IP地址为{ip_address}", "plain", "utf-8")
        message["From"] = Header(sender)

        if isinstance(receivers, list):
            message['To'] = Header(",".join(receivers), "utf-8")
        else:
            message['To'] = Header(receivers, "utf-8")

        subject = f"[{hostname}]IP地址或主机名发生变化"
        message["Subject"] = Header(subject, "utf-8")

        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            smtpObj.quit()
            return True
        except smtplib.SMTPException:
            return False

    def check_wifi_state(self):
        if self.iface.status() == pywifi.const.IFACE_CONNECTED:
            return True
        else:
            return False

    def get_current_wifi_ssid(self):
        if current_os == "win32":
            if self.check_wifi_state():
                cmd = "netsh wlan show interfaces"
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = result.stdout.decode("gbk")
                result = result.split("\r\n")
                for i in result:
                    if "SSID" in i:
                        return i.split(":")[1].strip()
            else:
                return None
        elif current_os == "linux":
            if self.check_wifi_state():
                cmd = "iwgetid"
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = result.stdout.decode("utf-8")
                result = result.split("\n")
                for i in result:
                    if "ESSID" in i:
                        return i.split('"')[1]
            else:
                return None

    def connect_to_wifi(self):
        self.iface.disconnect()
        time.sleep(1)

        profile = pywifi.Profile()
        profile.ssid = self.network_ssid
        profile.auth = pywifi.const.AUTH_ALG_OPEN
        profile.akm.append(pywifi.const.AKM_TYPE_NONE)

        self.iface.remove_all_network_profiles()

        tmp_profile = self.iface.add_network_profile(profile)

        self.iface.connect(tmp_profile)

        start_time = time.time()
        while time.time() - start_time < self.max_wait_time:
            if self.iface.status() == pywifi.const.IFACE_CONNECTED:
                return True
            time.sleep(1)

        return False

    def login(self):
        payload = {
            "user": self.username,
            "pass": self.password,
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        }
        response = requests.post('http://' + self.url + '/login', payload, headers=headers).status_code
        return response

    def logout(self):
        response = requests.get(self.url + "/logout").status_code
        return response

    def run(self):
        if self.enable_wifi_connect:
            if self.check_wifi_state():
                if self.get_current_wifi_ssid() != self.network_ssid:
                    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 尝试连接{self.network_ssid} Wi-Fi网络")
                    ret = self.connect_to_wifi()
                    if ret:
                        response = self.login()
                        if response == 200:
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接成功")
                        else :
                            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
                    else :
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')} 尝试连接{self.network_ssid}] Wi-Fi网络")
                ret = self.connect_to_wifi()
                if ret:
                    response = self.login()
                    if response == 200:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接成功")
                    else:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
                else:
                    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
        else:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi 连接功能已关闭")
        if check_internet_connection():
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 已连接到互联网")
        else:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 未连接到互联网")
            if self.enable_wifi_reconnect:
                ret = self.connect_to_wifi()
                if ret:
                    response = self.login()
                    if response == 200:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接成功")
                    else:
                        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
                else:
                    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi网络连接失败")
            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Wi-Fi 重连功能已关闭")
        if self.check_ip():
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] IP地址或主机名发生变化")
            if self.enable_mail_notification:
                self.mail_notification(self.last_host_name, self.last_ip_address)
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 邮件通知功能已开启,已发送邮件")
            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 邮件通知功能已关闭")
        else:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] IP地址或主机名未发生变化")

    def set_enable_wifi_connect(self, param):
        self.enable_wifi_connect = param
        self.config["enable_wifi_connect"] = param
        yaml_process.write_config(self.config)

    def set_enable_wifi_reconnect(self, param):
        self.enable_wifi_reconnect = param
        self.config["enable_wifi_reconnect"] = param
        yaml_process.write_config(self.config)

    def set_enable_mail_notification(self, param):
        self.enable_mail_notification = param
        self.config["enable_mail_notification"] = param
        yaml_process.write_config(self.config)

    def set_wifi_account(self, username, password):
        self.username = username
        self.password = password
        self.config["wifi_config"]["username"] = username
        self.config["wifi_config"]["password"] = password
        yaml_process.write_config(self.config)

    def set_mail_account(self, user, password):
        self.config["mail_config"]["mail_user"] = user
        self.config["mail_config"]["mail_pass"] = password
        self.config["mail_config"]["sender"] = user
        yaml_process.write_config(self.config)

    def set_mail_receiver(self, param):
        self.config["mail_config"]["receivers"] = param

    def set_mail_smtp(self, host, port):
        self.config["mail_config"]["mail_host"] = host
        self.config["mail_config"]["mail_port"] = port
        yaml_process.write_config(self.config)

    def set_receivers(self, param):
        self.config["mail_config"]["receivers"] = param
        yaml_process.write_config(self.config)

    def get_wifi_config(self):
        return self.config["wifi_config"]


def check_first_run():
    data_file = "data.yaml"
    config_file = "config.yaml"

    if os.path.exists(data_file) and os.path.exists(config_file):
        return True
    else:
        data = {"last_host_name": socket.gethostname(),
                "last_ip_address": socket.gethostbyname(socket.gethostname()),
                "url": "10.3.8.211",
                "portal_SSID": "BUPT-portal"
                }
        config = {"enable_mail_notification": True,
                  "enable_wifi_connect": True,
                  "enable_wifi_reconnect": True,
                  "max_wait_time": 10,
                  "wifi_config":
                      {
                          "username": "",
                          "password": ""
                      },
                  "mail_config":
                      {
                          "mail_host": "smtp.exmail.qq.com",
                          "mail_port": 465,
                          "mail_user": "",
                          "mail_pass": "",
                          "sender": "",
                          "receivers": []
                      },
                  }
        print("未找到配置文件，已自动生成配置文件模板")
        yaml_process.write_data(data)
        yaml_process.write_config(config)
        return False


if __name__ == "__main__":
    if not check_first_run():
        print("请编辑配置文件后重新运行程序")
        exit(0)
    fsm = AUTOFSM()
    while True:
        fsm.run()
        time.sleep(30)
