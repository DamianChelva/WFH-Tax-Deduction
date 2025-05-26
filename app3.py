from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.form.to_dict(flat=False)
    section1_items = []
    section1_total = 0
    section2_total = 0

    # Process Section 1 items
    for i in range(len(data['item[]'])):
        item = data['item[]'][i]
        usage = float(data['usage[]'][i])
        rate = float(data['rate[]'][i])
        type_ = data['type[]'][i]
        if type_ == 'monthly':
            monthly = rate * (usage / 100)
            annual = monthly * 12
        else:
            hours_week = float(data['hours_week[]'][i])
            kwh = float(data['kwh[]'][i])
            monthly = hours_week * 4 * kwh * rate
            annual = monthly * 12 * (48 / 52)

        section1_total += annual
        section1_items.append({
            'Item': item,
            'Usage %': usage,
            'Rate': rate,
            'Monthly Cost': round(monthly, 2),
            'Annual Cost': round(annual, 2)
        })

    # Process Section 2 (occupancy)
    try:
        rent_per_week = float(data['rent_per_week'][0])
        floor_percentage = float(data['floor_percentage'][0])
        rent_total = rent_per_week * 48
        section2_total = rent_total * (floor_percentage / 100)
    except:
        rent_per_week = 0
        floor_percentage = 0

    return render_template('index.html',
                           section1_items=section1_items,
                           section1_total=round(section1_total, 2),
                           section2_total=round(section2_total, 2),
                           rent_total=rent_per_week * 48,
                           rent_per_week=rent_per_week,
                           floor_percentage=floor_percentage)

@app.route('/export', methods=['POST'])
def export():
    data = request.form.to_dict(flat=False)
    section1_rows = []
    section1_total = 0
    section2_total = 0

    for i in range(len(data['item[]'])):
        item = data['item[]'][i]
        usage = float(data['usage[]'][i])
        rate = float(data['rate[]'][i])
        type_ = data['type[]'][i]

        if type_ == 'monthly':
            monthly = rate * (usage / 100)
            annual = monthly * 12
        else:
            hours_week = float(data['hours_week[]'][i])
            kwh = float(data['kwh[]'][i])
            monthly = hours_week * 4 * kwh * rate
            annual = monthly * 12 * (48 / 52)

        section1_total += annual
        section1_rows.append([item, usage, rate, round(monthly, 2), round(annual, 2)])

    try:
        rent_per_week = float(data['rent_per_week'][0])
        floor_percentage = float(data['floor_percentage'][0])
        rent_total = rent_per_week * 48
        section2_total = rent_total * (floor_percentage / 100)
    except:
        rent_total = 0
        floor_percentage = 0

    # Create Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df1 = pd.DataFrame(section1_rows, columns=['Item', 'Usage %', 'Rate', 'Monthly Cost', 'Annual Cost'])
    df1.loc[len(df1.index)] = ['Total', '', '', '', round(section1_total, 2)]
    df1.to_excel(writer, sheet_name='Running Expenses', index=False)

    df2 = pd.DataFrame([{
        'Rent Per Week': rent_per_week,
        'Total Rent (48 weeks)': rent_total,
        'Floor Area %': floor_percentage,
        'Occupancy Deduction': round(section2_total, 2)
    }])
    df2.to_excel(writer, sheet_name='Occupancy Expenses', index=False)

    writer.close()
    output.seek(0)
    return send_file(output, download_name="wfh_tax_deduction_24_25.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

