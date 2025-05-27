from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from fetch_data import lookup


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

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
        return render_template('index.html', logged_in=True)
    else:
        return render_template('index.html')
    
@app.route('/test')
def test():
    return render_template('animationtest.html')

# -------------------------------------- WORKING ON THESE FIRST ----------------------------------------
# When the user first visits the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Display the login page
        return render_template('login.html')
    else:
        # Handle the login form submission
        if not request.form.get("username"):
            return render_template('login.html', error="Missing username.")
        if not request.form.get("password"):
            return render_template('login.html', error="Missing password.")

        username = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        conn.close()
        if len(rows) == 0:
            return render_template('login.html', error="Username not found.")
        
        user = rows[0]
        user_id = user[0]
        user_name = user[1]
        pw_hash = user[2]

        if not check_password_hash(pw_hash, password):
            return render_template('login.html', error="Incorrect password.")
        
        session['user_id'] = user_id

        return redirect('/dashboard')
# Alias
@app.route('/signin')
def signin():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # Handle the registration form submission
        if not request.form.get("username"):
            return render_template('register.html', error="Missing username.")
        if not request.form.get("password"):
            return render_template('register.html', error="Missing password.")
        if not request.form.get("confirm_password"):
            return render_template('register.html', error="Missing confirm password.")

        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        db.close()

        if len(rows) > 0:
            return render_template('register.html', error=f"Account with username '{username}' already exists already exists.")
        
        pw_hash = generate_password_hash(password)

        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, pw_hash) VALUES (?, ?)", (username, pw_hash))
        db.commit()
        db.close()
        
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        db.close()

        if len(rows) == 0:
            return render_template('register.html', error="Failed to create account. Please try again later.")
        
        user = rows[0]
        user_id = user[0]
        password = user[2]
        session['user_id'] = user_id

        return redirect('/dashboard')
# Aliases
@app.route('/signup')
def redirect_register():
    return redirect('/register')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
#------------------------------------------------------------------------------------------------------


@app.route('/dashboard')
def dashboard():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('dashboard.html', logged_in=True)

# Searches will use /search?symbol=<symbol>
@app.route('/search')
def search():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('search.html', logged_in=True)

# Portfolio will display a list of all the person's current stocks
# Each entry will show {symbol, price, total share count}
# Clicking the symbol will take you to the /search?symbol=<symbol>
@app.route('/portfolio')
def portfolio():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('portfolio.html', logged_in=True)

# A list of everyone who has completed at least one round sorted by fastest to slowest.
@app.route('/leaderboard')
def leaderboard():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('leaderboard.html', logged_in=True)

@app.route('/watchlist')
def watchlist():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('watchlist.html', logged_in=True)



@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset-password.html')
    else:
        return render_template('reset-password.html', error="This feature is not implemented yet.")




@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico')
def favicon():
    return send_from_directory('/static/images', 'favicon.ico')

@app.route('/<path:unknown_path>')
def unknown_path(unknown_path):
    if request.cookies.get('session'):
        return render_template('404.html', path=unknown_path, logged_in=True), 404
    return render_template('404.html', path=unknown_path), 404



if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), port=os.getenv("PORT"))