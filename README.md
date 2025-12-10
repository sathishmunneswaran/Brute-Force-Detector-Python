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
git clone https://github.com//Brute-Force-Detector-Python.git
cd Brute-Force-Detector-Python

APP_EMAIL=your_email@gmail.com
APP_PASS=your_app_password


