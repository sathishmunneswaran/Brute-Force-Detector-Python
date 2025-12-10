import re
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
# === CONFIG ===
LOG_FILE = "logs.txt"      # later /var/log/auth.log use pannalaam
THRESHOLD_HIGH = 10        # 10+ attempts = HIGH
THRESHOLD_MED  = 5         # 6–10 = MEDIUM

# ---- Same helper functions you already have ----

FAIL_KEYWORDS = [
    "Failed password",
    "authentication failure",
    "Invalid user",
    "Failed login",
    "Login failed",
    "denied",
    "Rejected"
]

def is_failed_event(line):
    return any(keyword in line for keyword in FAIL_KEYWORDS)

def is_private_ip(ip):
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        (ip.startswith("172.") and 16 <= int(ip.split(".")[1]) <= 31)
    )

def get_geoip(ip):
    if is_private_ip(ip):
        return "Private Network (Internal Attacker)"
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=4).json()
        if response.get("status") == "success":
            return f"{response.get('country')} ({response.get('city')})"
        else:
            return "Unknown Location"
    except:
        return "GeoIP Lookup Failed"

def send_email_alert(attacker_ip, attempts, location, severity):
    sender_email = os.getenv("APP_EMAIL")
    sender_password = os.getenv("APP_PASS")
    receiver_email = os.getenv("APP_EMAIL")

    subject = f"[ALERT] Brute Force Detected from {attacker_ip}"
    body = f"""
Brute Force Attack Detected!

Attacker IP: {attacker_ip}
Attempts: {attempts}
Severity: {severity}
Location: {location}

This alert was generated automatically by the SOC Failed Login Detector.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"📧 Email Alert Sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")


# === GLOBAL STATE ===
failed_count = 0
ip_list = {}
already_alerted = set()     # ip’s we already sent HIGH alert for
report_content = []


def process_line(line):
    """One log line-ku detection logic apply pannum."""
    global failed_count, ip_list, report_content, already_alerted

    if not is_failed_event(line):
        return

    failed_count += 1

    ip_match = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
    if not ip_match:
        return

    ip = ip_match[0]
    ip_list[ip] = ip_list.get(ip, 0) + 1
    count = ip_list[ip]

    # Severity
    if count > THRESHOLD_HIGH:
        status = "HIGH - Brute Force"
    elif count > THRESHOLD_MED:
        status = "MEDIUM - Possible Attack"
    else:
        status = "LOW - Minor Failed Attempts"

    location = get_geoip(ip)

    print(f"[LIVE] {ip} -> {count} attempts -> {status} -> {location}")

    # Email only for first time HIGH alert per IP
    if "HIGH" in status and ip not in already_alerted:
        send_email_alert(ip, count, location, status)
        already_alerted.add(ip)

    # Minimal report in memory (if you want, you can periodically dump to file)
    report_content.append(f"{datetime.now()} | {ip} -> {count} -> {status} -> {location}")


def monitor_log(filepath):
    """Real-time tail -f style log monitoring."""
    print(f"\n[+] Starting real-time monitoring on: {filepath}")
    print("[+] Waiting for new log lines...\n")

    with open(filepath, "r") as f:
        # Move to end of file – old entries skip pannuvom
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                # No new line yet – little wait
                time.sleep(0.5)
                continue

            # New log line came
            process_line(line)


if __name__ == "__main__":
    try:
        monitor_log(LOG_FILE)
    except KeyboardInterrupt:
        # Ctrl+C pressed – program stop
        print("\n\n[!] Stopped monitoring.")
        print(f"Total Failed Attempts seen: {failed_count}")
        print("Final IP counts:", ip_list)
