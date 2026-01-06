# Work From Home Tax Deduction Calculator

A web-based calculator for Australian Work From Home tax deductions using the **Actual Method** for FY 2024-25.

## Features

- **Section 1: Running Expenses**
  - Internet and mobile phone costs
  - Electricity costs for laptop, monitors, air conditioning, and lighting
  - Office supplies (max $300)
  - Cleaning expenses (max $250)
  - Dynamic item addition with pre-configured electricity rates

- **Section 2: Occupancy Expenses**
  - Rent-based calculations
  - Work area percentage calculations
  - CGT implications warning

- **Interactive Interface**
  - Add/remove expense items dynamically
  - Real-time calculations
  - ATO reference links
  - Comprehensive disclaimer

## Installation

1. Clone or download this repository
2. Install Flask:
   ```bash
   pip install flask
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Use the calculator:
   - Add expense items using the dropdown
   - Enter your usage percentages and rates
   - Calculate section totals
   - View combined deduction amount

## File Structure

```
WFH-Tax-Deduction/
├── app.py              # Flask application
├── wsgi.py            # WSGI configuration
├── templates/
│   ├── form.html      # Main calculator interface
│   └── logs.html      # Access logs template
└── README.md          # This file
```

## Important Notes

- This calculator is for **guidance only** and does not constitute tax advice
- Based on ATO Actual Method for FY 2024-25
- **Warning**: Claiming occupancy expenses may trigger Capital Gains Tax obligations
- Consult a qualified tax professional for personalized advice

## Developer

**Damian Chelvarajan**  
Email: damian_lk@hotmail.com

## Disclaimer

This tool provides general guidance based on ATO regulations. Users should consult with registered tax agents or qualified accountants for personal tax situations. No liability is accepted for any loss or damage from using this calculator.