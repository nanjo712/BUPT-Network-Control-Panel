# BUPT-Network-Control-Panel (Developing)

A control panel for BUPT School Network

一个用于北邮校园网的控制面板

Mainly used for automatically connecting to BUPT-portal and sending email notification when IP changes

主要适用于自动化连接BUPT-portal并在IP变动时发送邮件通知

Focused on solve the problem of SSH and remote desktop connection to the school network

用于解决校园网下SSH和远程桌面连接的问题

The CLI version is tested on Windows 11 and Ubuntu 20.04. It should work on other Linux distributions and Windows 10.

CLI版本在Windows 11和Ubuntu 20.04上测试通过，应该可以在其他Linux发行版和Windows 10上运行。

The GUI version is tested on Windows 11. It should work on Windows 10.

GUI版本在Windows 11上测试通过，应该可以在Windows 10上运行。

PyQt6 installation is required for GUI version. But it seems that PyQt6 is not available on Ubuntu 20.04. At least I can't install it.

GUI版本需要PyQt6，但是似乎Ubuntu 20.04上没有PyQt6。至少我没法安装。

## Supported

- Automatically connect to BUPT-portal
- Send email notification when IP changes

- 自动化连接BUPT-portal
- 检测IP变动并发送邮件通知

## Usage-CLI

### 1. Install

```bash
git clone https://github.com/nanjo712/BUPT-Network-Control-Panel.git
```

### 2. Config

At your first run, the program will generate a "data.yaml" file and a "config.yaml" file

第一次运行时，程序会生成一个"data.yaml"文件和一个"config.yaml"文件

You should edit "config.yaml" before you run the program again

你应该在再次运行程序之前修改"config.yaml"

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

It's notable that you should run it as root by adding "sudo" before the command.

需要注意的是，你应该以root权限运行它，即在命令前加上"sudo"

To use it easily, you can add it to startup application

为了方便使用，你可以将它添加到开机启动项

## Usage-GUI

### 1. Install

```bash
git clone https://github.com/nanjo712/BUPT-Network-Control-Panel.git
```

### 2. Run

```bash
python3 guiBringup.py
```

## TODO

- Automatically connect to BUPT-mobile
- Develop a GUI

- 自动化连接BUPT-mobile
- 开发图形界面，简化使用

## License

GPLv3 License




