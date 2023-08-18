# BUPT-Network-Control-Panel (Developing)

A control panel for BUPT School Network

一个用于北邮校园网的控制面板

Mainly used for automatically connecting to BUPT-portal and sending email notification when IP changes

主要适用于自动化连接BUPT-portal并在IP变动时发送邮件通知

Focused on solve the problem of SSH and remote desktop connection to the school network

用于解决校园网下SSH和远程桌面连接的问题

## Supported

- Automatically connect to BUPT-portal
- Send email notification when IP changes

- 自动化连接BUPT-portal
- 检测IP变动并发送邮件通知

## Usage

### 1. Install

```bash
git clone https://github.com/nanjo712/BUPT-Network-Control-Panel.git
```

### 2. Config

Edit "config.yaml" as the instruction in the file

按照文件中的说明修改"config.yaml"

It's not recommended to use your own email account to send notification, because the password will be stored in plain
text

不建议使用自己的邮箱账号发送通知，因为密码会以明文形式存储

Edit "data.yaml" is also not recommended unless you know what you are doing

除非你知道自己在做什么，否则不建议修改"data.yaml"

### 3. Run

```bash
python3 main.py
```

To use it easily, you can add it to startup application

为了方便使用，你可以将它添加到开机启动项

## TODO

- 自动化连接BUPT-mobile
- 打包为CLI工具，简化使用
- 开发图形界面，简化使用


