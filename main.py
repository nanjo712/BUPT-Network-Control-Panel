import time
import yaml_process
import ip_check
import portal_connect

config = yaml_process.read_config()
data = yaml_process.read_data()

if portal_connect.check_wifi_state() and portal_connect.check_internet_connection():
    print("Wi-Fi 已连接，网络正常")
else:
    wifi_config = config["wifi_config"]
    username = wifi_config["username"]
    password = wifi_config["password"]
    url = data["url"]
    network_ssid = data["portal_SSID"]
    response = 0
    while response != 200:
        print("网络未连接，正在尝试连接")
        portal_connect.connect_to_wifi(network_ssid)
        response = portal_connect.login(username, password)
    print("登录请求已发送成功")

while True:
    if portal_connect.check_internet_connection():
        print("网络连接正常")
    else:
        print("网络连接异常")
        continue
    if ip_check.check_ip(data):
        print("IP地址或主机名发生变化")
        if config["enable_mail_notification"]:
            ip_check.mail_notification(data["last_host_name"], data["last_ip_address"])
        print(f"当前主机名：{data['last_host_name']}，当前IP地址：{data['last_ip_address']}")
    else:
        print("IP地址或主机名未发生变化")
    time.sleep(60)
