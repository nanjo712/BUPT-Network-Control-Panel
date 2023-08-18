import time
import yaml_process
import ip_check
import portal_connect

config = yaml_process.read_config()
data = yaml_process.read_data()

if portal_connect.check_wifi_state():
    print("Wi-Fi 已连接，无需连接")
else:
    print("Wi-Fi 未连接，正在连接")
    wifi_config = config["wifi_config"]
    username = wifi_config["username"]
    password = wifi_config["password"]
    url = data["url"]
    network_ssid = data["portal_SSID"]
    while not portal_connect.check_wifi_state():
        portal_connect.connect_to_wifi(network_ssid)
        response = portal_connect.login(username, password)
        if response == 200:
            print("请求成功")
            break
        else:
            print("请求失败")

while True:
    if portal_connect.check_internet_connection():
        print("网络连接正常")
    else:
        print("网络连接异常")
        exit(1)
    if ip_check.check_ip(data):
        print("IP地址或主机名发生变化")
        if config["enable_mail_notification"]:
            ip_check.mail_notification(data["last_host_name"], data["last_ip_address"])
        print(f"当前主机名：{data['last_host_name']}，当前IP地址：{data['last_ip_address']}")
    else:
        print("IP地址或主机名未发生变化")
    time.sleep(60)
