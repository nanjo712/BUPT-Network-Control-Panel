import yaml_process
import pywifi
import socket
import smtplib
import time
import requests
import subprocess
import os
from email.mime.text import MIMEText
from email.header import Header
import urllib.request
import urllib.error


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

    def check_ip(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
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
                    print(f"尝试连接{self.network_ssid} Wi-Fi网络")
                    ret = self.connect_to_wifi()
                    if ret:
                        response = self.login()
                        if response == 200:
                            print("Wi-Fi网络连接成功")
                        else :
                            print("Wi-Fi网络连接失败")
                    else :
                        print("Wi-Fi网络连接失败")
            else:
                print(f"尝试连接{self.network_ssid} Wi-Fi网络")
                ret = self.connect_to_wifi()
                if ret:
                    response = self.login()
                    if response == 200:
                        print("Wi-Fi网络连接成功")
                    else:
                        print("Wi-Fi网络连接失败")
                else:
                    print("Wi-Fi网络连接失败")
        else:
            print("Wi-Fi 连接功能已关闭")
            exit(0)
        if check_internet_connection():
            print("已连接到互联网")
        else:
            print("未连接到互联网")
            if self.enable_wifi_reconnect:
                self.connect_to_wifi()
                self.login()
            else:
                print("Wi-Fi 重连功能已关闭")
                exit(0)

        if self.check_ip():
            print("IP地址或主机名发生变化")
            if self.enable_mail_notification:
                self.mail_notification(self.last_host_name, self.last_ip_address)
                print("邮件通知功能已开启,已发送邮件")
            else:
                print("邮件通知功能已关闭")
        else:
            print("IP地址或主机名未发生变化")


data_file = "data.yaml"
config_file = "config.yaml"

if os.path.exists(data_file) and os.path.exists(config_file):
    pass
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
                      "receivers": [""]
                  },
              }
    print("未找到配置文件，已自动生成配置文件，请修改配置文件后重新运行程序")
    yaml_process.write_data(data)
    yaml_process.write_config(config)
    exit(0)

fsm = AUTOFSM()
while True:
    fsm.run()
    time.sleep(30)
