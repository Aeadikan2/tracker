from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from logic import BudgetManager
from models import BudgetConfig
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages
manager = BudgetManager()

@app.route('/')
def index():
    # Helper to get today's date for default value
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    stats = manager.get_monthly_stats()
    return render_template('index.html', today=today, stats=stats)

@app.route('/add', methods=['POST'])
def add_income():
    try:
        amount = float(request.form['amount'])
        date_str = request.form['date']
        
        if amount <= 0:
            flash('Amount must be positive.', 'error')
            return redirect(url_for('index'))
            
        entry = manager.add_income(amount, date_str)
        flash(f'Income added successfully! Savings: ₦{entry.savings:.2f}', 'success')
        return redirect(url_for('index'))
    except ValueError:
        flash('Invalid input.', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    entries = manager.get_history()
    # Sort entries by date descending
    entries.sort(key=lambda x: x.date, reverse=True)
    return render_template('history.html', entries=entries)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        try:
            savings = float(request.form['savings']) / 100
            expenses = float(request.form['expenses']) / 100
            investments = float(request.form['investments']) / 100
            discretionary = float(request.form['discretionary']) / 100
            
            if manager.update_settings(savings, expenses, investments, discretionary):
                flash('Settings updated successfully!', 'success')
            else:
                flash('Error: Percentages must sum to 100%.', 'error')
        except ValueError:
            flash('Invalid input.', 'error')
        return redirect(url_for('settings'))
        
    config = manager.config
    # Pass percentages as 0-100 for the form
    return render_template('settings.html', 
                           savings=int(config.savings_pct*100),
                           expenses=int(config.expenses_pct*100),
                           investments=int(config.investments_pct*100),
                           discretionary=int(config.discretionary_pct*100))

@app.route('/api/stats')
def api_stats():
    return jsonify(manager.get_monthly_stats())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
