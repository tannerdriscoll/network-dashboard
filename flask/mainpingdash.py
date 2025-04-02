from flask import Flask, render_template, jsonify
import os
import platform
import sqlite3
import datetime

#create flask app instance
app = Flask(__name__)

# List of devices to monitor
devices = {
    "MX-FW": "192.168.128.1",
    "K8s Master Node": "10.20.15.21",
    "K8s Worker Node": "10.20.15.20",
    "ProxMox Node 1": "10.20.15.18",
    "proxMox Node 2": "10.20.15.19",
}
DB_NAME='ping_data.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    device_name TEXT NOT NULL,
                                    ip_address TEXT NOT NULL,
                                    status TEXT NOT NULL,
                                    timestamp TEXT NOT NULL)''')
        conn.commit()
init_db()


#function that takes device name and ip address from dic, and uses the os module to execute a ping from the command line, returns online or offline status
def ping_device(device_name, ip):
    """Pings a device and returns 'Online' or 'Offline'."""
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 1 {ip} > nul")  # Windows: '-n 1'
    else:
        response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")  # Linux/macOS: '-c 1'

    status="Online" if response == 0 else "Offline"
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #store result in db
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (device_name, ip_address, status, timestamp) VALUES (?, ?, ?, ?)",
                       (device_name, ip, status, timestamp))
        conn.commit()
    return status

count=0
for i in devices:
    count+=1
#function to pull ping history from sqlite db using sql
def get_ping_history(limit=count):
    """Retrieves the latest ping results."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT device_name, ip_address, status, timestamp FROM devices ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

#define route for homepage
@app.route('/')
def dashboard():
    history=get_ping_history()
    return render_template("index.html", history=history, devices=devices)

@app.route('/ping')
def ping():
    statuses = {name: ping_device(name, ip) for name, ip in devices.items()}
    return jsonify(statuses=statuses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





#Next steps

#Add more features like SSH commands with Netmiko.
#Store data in a database (SQLite/MySQL).-----------------------------------
#Display network graphs with Chart.js.
#Style it using Bootstrap or Tailwind CSS for a cleaner UI.
#Add authentication using Flask-Login for secure access.
#Integrate SSH automation with Netmiko to send commands to devices.
#Visualize data using Chart.js to show uptime trends.