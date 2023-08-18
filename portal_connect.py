import requests
import yaml_process
import urllib.request
import pywifi
from pywifi import const
import time

max_wait_time = 10
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]
config = yaml_process.read_config()["wifi_config"]
data = yaml_process.read_data()
username = config["username"]
password = config["password"]
url = data["url"]
network_ssid = data["portal_SSID"]


def check_wifi_state():
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


def connect_to_wifi(ssid):
    global wifi
    global iface

    # 断开当前连接
    iface.disconnect()
    time.sleep(1)

    # 创建连接文件
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)

    # 删除所有的连接文件
    iface.remove_all_network_profiles()

    # 添加连接文件
    tmp_profile = iface.add_network_profile(profile)

    # 开始连接
    iface.connect(tmp_profile)

    # 等待连接成功
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        if iface.status() == const.IFACE_CONNECTED:
            print(f"成功连接到 Wi-Fi 网络: {ssid}")
            return True
        time.sleep(1)

    print("连接超时，无法连接到 Wi-Fi 网络")
    return False


def check_internet_connection():
    try:
        urllib.request.urlopen('https://www.baidu.com', timeout=1)
        return True
    except urllib.error.URLError:
        return False


def login(username, password):
    payload = {
        "user": username,
        "pass": password,
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    global url
    response = requests.post('http://' + url + '/login', payload, headers=headers).status_code
    return response


def logout():
    response = requests.get(url + "/logout").status_code
    return response


if __name__ == '__main__':
    connect_to_wifi(network_ssid)
    response = login(username, password)
    if response == 200:
        print("Request Success")
    else:
        print("Request Failed")
    if check_internet_connection():
        print("Internet Connection OK")
    else:
        print("Internet Connection Failed")
