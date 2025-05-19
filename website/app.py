from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
import os
import sqlite3

from fetch_data import lookup


load_dotenv()
app = Flask(__name__)

db_path = os.getenv("DB_PATH")
if not db_path:
    raise ValueError("DB_PATH environment variable is not set.")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found at {db_path}.")
if not os.access(db_path, os.R_OK):
    raise PermissionError(f"Database file at {db_path} is not readable.")


# Before anything loads, if the person is not signed in, direct them to /
# Then give a small popup saying "You are not logged in: Log in to access the rest of the websites"
# Then they can click login or register at the top (and not be redirected)
# Once logged in direct them to /dashboard

@app.route('/')
def index():
    if session.get('user_id') is not None:
        return render_template('index.html')
    else:
        return render_template('index.html')
    
@app.route('/test')
def test():
    return render_template('animationtest.html')

# -------------------------------------- WORKING ON THESE FIRST ----------------------------------------
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def loginPost():
    # Set cookies
    return redirect('/')
# Aliases
@app.route('/signin')
def signin():
    return redirect('/login')

@app.route('/register')
def register():
    return render_template('register.html')
# Aliases
@app.route('/signup')
def redirect_register():
    return redirect('/register')
# ------------------------------------------------------------------------------------------------------


@app.route('/dashboard')
def dashboard():
    if request.cookies.get('user_id') is None:
        return redirect('/')
    return render_template('dashboard.html')

# Searches will use /search?symbol=<symbol>
@app.route('/search')
def search():
    if request.cookies.get('user_id') is None:
        return redirect('/')
    return render_template('search.html')

# Portfolio will display a list of all the person's current stocks
# Each entry will show {symbol, price, total share count}
# Clicking the symbol will take you to the /search?symbol=<symbol>
@app.route('/portfolio')
def portfolio():
    if request.cookies.get('user_id') is None:
        return redirect('/')
    return render_template('portfolio.html')

# A list of everyone who has completed at least one round sorted by fastest to slowest.
@app.route('/leaderboard')
def leaderboard():
    if request.cookies.get('user_id') is None:
        return redirect('/')
    return render_template('leaderboard.html')




if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), port=os.getenv("PORT"))