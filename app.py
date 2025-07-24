from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'expenses.csv'

def init_csv():
    try:
        with open(CSV_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    except FileExistsError:
        pass

@app.route('/')
def index():
    expenses = []
    total = 0.0
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['Amount'] = float(row['Amount'])
                total += row['Amount']
                expenses.append(row)
            except (KeyError, ValueError) as e:
                print(f"Skipping row due to error: {e} - {row}")
    return render_template('index.html', expenses=expenses, total=total)


@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d")
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, description])
        return redirect('/')
    return render_template('add_expense.html')

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)
