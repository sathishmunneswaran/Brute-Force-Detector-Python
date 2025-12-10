# 🔐 Brute Force Detector – Python (Real-Time Log Monitoring)

A real-time **Brute Force Attack Detection System** built using Python.  
This tool continuously monitors Linux authentication logs, detects failed login patterns, classifies severity levels, performs GeoIP lookup for attacker IPs, and sends **automatic email alerts** for high-severity attacks.

---

## 🚀 Features

### ✅ Real-Time Monitoring  
Monitors log files like:
- `logs.txt` (test file)
- `/var/log/auth.log` (real Linux SSH logs)

### ✅ Intelligent Detection  
Detects failed login attempts using keywords:
- Failed password  
- Authentication failure  
- Invalid user  
- Login failed  

### ✅ Severity Classification  
| Attempts | Severity | Meaning |
|---------|----------|---------|
| 1–5     | LOW      | Normal failed attempts |
| 6–10    | MEDIUM   | Suspicious behavior |
| 10+     | HIGH     | Brute Force Attack |

### ✅ GeoIP Lookup  
Shows attacker location:  
**Country + City**  
Internal/private IPs are automatically flagged as:  
`Private Network (Internal Attacker)`

### ✅ Email Alert System  
Automatically sends alert when attack becomes **HIGH severity**:
- Attacker IP  
- Number of attempts  
- Severity  
- GeoIP location  

### 📧 SMTP (Gmail) Supported  
Environment variables:
---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/sathishmunneswaran/Brute-Force-Detector-Python.git
cd Brute-Force-Detector-Python

APP_EMAIL=your_email@gmail.com
APP_PASS=your_app_password
```
### 2️⃣ Install Requirements
```bash
export APP_EMAIL="your_email@gmail.com"
export APP_PASS="your_gmail_app_password"
```
### ▶️ Usage:
### Run the script:
```bash
python3 brute_force_detector.py
```
### Real server monitoring:
### Edit:
```bash
LOG_FILE = "/var/log/auth.log"
```
### Then:
```bash
sudo python3 brute_force_detector.py
```
### 📊 Sample Output
```bash
[LIVE] 185.244.25.42 -> 6 attempts -> MEDIUM - Possible Attack -> Russia (Moscow)
[LIVE] 185.244.25.42 -> 11 attempts -> HIGH - Brute Force -> Russia (Moscow)
📧 Email Alert Sent
```
### 🧱 Project Structure
```bash
Brute-Force-Detector-Python/
│── brute_force_detector.py
│── logs.txt
│── README.md
```
### 🔥 Future Enhancements
Dashboard with charts

Store attack logs in SQLite

Auto-block attacker IP with iptables

Telegram/Slack alert integration

Multithreading for faster GeoIP
### 👨‍💻 Author
Sathish Muneeswaran
Cybersecurity Enthusiast | SOC Analyst (Learning)

