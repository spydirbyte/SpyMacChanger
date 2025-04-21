# 🕵️‍♂️ SPY MAC Changer
> MAC Address Changer — developed by **AnonSpyDir**

---

## 🎯 Overview

**SPY MAC Changer** is a Python based spoofing tool that allows you to easily change your device’s MAC address — manually or randomly — using either a sleek interactive menu or command line flags.

This tool is perfect for privacy enthusiasts, penetration testers, and anyone who wants to mask their device identity on a network.

---

## ⚙️ Features

✅ Interactive numbered menu system  
✅ Auto Detects network interfaces  
✅ Random MAC address generation  
✅ Manual MAC spoofing  
✅ Command line mode
✅ Logs all spoofing attempts to `spylog.txt`  

---

## 🧰 Requirements

- Python 3.x
- Linux or macOS (tested on Debian, Kali, Ubuntu)
- Root/sudo access to change MAC
- `ifconfig` must be available (usually pre-installed)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 How to Use

### 🔢 Option 1: Interactive Mode

Just launch the tool without any arguments:

```bash
sudo python3 spymac.py
```
You'll get a stylish hacker-style menu like this:

```bash
Available Interfaces:
1. eth0
2. wlan0

Choose an option:
1. Enter MAC manually
2. Generate random MAC
3. Exit
```
Enter numbers to navigate

🧠 Option 2: Command Line Mode
```bash
# Set a specific MAC address
sudo python3 spymac.py -i eth0 -m 00:11:22:33:44:55

# Set a random MAC address
sudo python3 spymac.py -i eth0 --random
```


📛 Disclaimer
This tool is for educational and privacy respecting purposes only.
Do not use it to impersonate devices or bypass network access controls.
You are responsible for your own actions.


