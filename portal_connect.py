import requests
import yaml
import urllib.request

url = 'http://10.3.8.211'


def check_internet_connection():
    try:
        urllib.request.urlopen('https://www.baidu.com', timeout=1)
        return True
    except urllib.error.URLError:
        return False


def login(username, password):
    data = {
        "user": username,
        "pass": password,
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    response = requests.post(url, data, headers=headers).status_code
    return response


def logout():
    response = requests.get(url + "/logout").status_code
    return response


if __name__ == '__main__':
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    username = config["username"]
    password = config["password"]
    response = login(username, password)
    if response == 200:
        print("Request Success")
    else:
        print("Request Failed")
    if check_internet_connection():
        print("Internet Connection OK")
    else:
        print("Internet Connection Failed")
