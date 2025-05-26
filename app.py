from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    form = request.form
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

if __name__ == '__main__':
    app.run()

