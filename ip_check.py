import yaml
import socket


def read_data():
    with open("data.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def read_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def check_ip(data):
    last_host_name = data["last_host_name"]
    last_ip_address = data["last_ip_address"]

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    if (hostname != last_host_name) or (ip_address != last_ip_address):
        print("IP地址或主机名发生变化，正在更新数据")
        data["last_host_name"] = hostname
        data["last_ip_address"] = ip_address
        with open("data.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)
        print("数据更新完成")
        return True, hostname, ip_address
    else:
        print("IP地址和主机名未发生变化")
        return False, hostname, ip_address


def mail_notification(hostname, ip_address):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    with open("config.yaml", "r", encoding="utf-8") as f:
        mail_config = yaml.safe_load(f)
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
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("邮件发送失败")


if __name__ == '__main__':
    data = read_data()
    config = read_config()
    enable_mail_notification = config["enable_mail_notification"]
    result, hostname, ip_address = check_ip(data)
    if enable_mail_notification and result:
        mail_notification(hostname, ip_address)
