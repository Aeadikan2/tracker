# Personal Income Tracker (₦)

A robust Python application to track monthly income and automatically split it according to the 50/30/10/10 budgeting rule. This project features both a **Command Line Interface (CLI)** and a modern **Web Interface** (Flask).

## Features

- **Automated Budgeting**: Automatically calculates splits for Savings (30%), Expenses (50%), Investments (10%), and Discretionary (10%).
- **Dual Interface**:
  - **CLI**: Fast, colorful terminal interface using `rich`.
  - **Web UI**: Modern, responsive dashboard using Flask and custom CSS.
- **Saves History**: Records all entries to a CSV file.
- **Customizable**: Adjust budget percentages to fit your needs.
- **Reporting**: View monthly breakdowns and cumulative statistics.
- **Currency**: Localized for Naira (₦).

## Installation

1. **Clone or Download** the repository.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows
   ./venv/Scripts/Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install pandas rich flask
   ```

## Usage

### Option 1: Web Interface (Recommended)
Launch the modern web dashboard:
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

### Option 2: Command Line Interface
Run the terminal version:
```bash
python main.py
```

## Project Structure

- `app.py`: Flask web application entry point.
- `main.py`: CLI application entry point.
- `logic.py`: Core business logic and calculations.
- `models.py`: Data models (`IncomeEntry`, `BudgetConfig`).
- `database.py`: CSV and JSON storage handling.
- `ui.py`: CLI interaction layer using `rich`.
- `templates/`: HTML templates for the web app.
- `static/`: CSS and JS files.

## Technology Stack

- **Python 3.8+**
- **Flask**: Web backend.
- **Rich**: Terminal formatting.
- **Pandas**: Data handling.
- **HTML5/CSS3**: Frontend design.
