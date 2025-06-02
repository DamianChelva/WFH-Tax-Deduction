from flask import Flask, render_template, request, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Secure user credentials (hashed password)
users = {
    "admin": generate_password_hash("1Qaz2wsx!@!007")
}

# File to store logs
LOG_FILE = "/var/log/wfhapp/access_logs.txt"

# IP addresses allowed to access /view_logs
ALLOWED_IPS = {"116.240.46.17"}  # <-- Replace with your actual IP(s)

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/', methods=['GET'])
def index():
    # Log access info
    ip = request.remote_addr
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    user_agent = request.headers.get('User-Agent', 'Unknown')

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | IP: {ip} | Agent: {user_agent}\n")

    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    form = request.form
    try:
        internet = float(form['internet_usage']) / 100 * float(form['internet_cost']) * 12
        laptop = float(form['laptop_hours']) * float(form['laptop_rate']) * 12
        monitor = float(form['monitor_hours']) * float(form['monitor_rate']) * 12
        aircon = float(form['aircon_hours']) * float(form['aircon_rate']) * 12
        mobile = float(form['mobile_usage']) / 100 * float(form['mobile_cost']) * 12
        supplies = float(form['supplies_cost'])
        cleaning = float(form['cleaning_usage']) / 100 * float(form['cleaning_cost'])

        running_expenses = sum([internet, laptop, monitor, aircon, mobile, supplies, cleaning])

        rent_total = float(form['rent_weekly']) * float(form['weeks_worked'])
        floor_area_ratio = float(form['floor_area']) / 100
        occupancy = rent_total * floor_area_ratio

        total = round(running_expenses + occupancy, 2)

        return render_template('form.html', result=total)

    except Exception as e:
        return render_template('form.html', error=f"Error: {e}")

@app.route('/view_logs', methods=['GET'])
@auth.login_required
def view_logs():
    ip = request.remote_addr
    if ip not in ALLOWED_IPS:
        abort(403)  # Forbidden

    if not os.path.exists(LOG_FILE):
        logs = ["No logs yet."]
    else:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()

    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run()
