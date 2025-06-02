import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, send_from_directory
from mailjet_rest import Client
import os
import random
import re
import requests
import sqlite3
import sqlite3 # Errors idk which
from werkzeug.security import generate_password_hash, check_password_hash

from mail import send_verification_email


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

debug = os.getenv("DEBUG", "false").lower() == "true"


db_path = os.getenv("DB_PATH")
if not db_path:
    raise ValueError("DB_PATH environment variable is not set.")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found at {db_path}.")
if not os.access(db_path, os.R_OK):
    raise PermissionError(f"Database file at {db_path} is not readable.")









# Config variables
start_capital = 1000000


'''
# Email
sender_email = os.getenv("SENDER_EMAIL")
sender_name = os.getenv("SENDER_NAME", "Money Pit")
mj_api_key_public = os.getenv("MJ_API_KEY_PUBLIC")
mj_api_key_private = os.getenv("MJ_API_KEY_PRIVATE")

if not sender_email:
    raise ValueError("SENDER_EMAIL environment variable is not set.")

mailjet = Client(auth=(mj_api_key_public, mj_api_key_private), version='v3.1')



def send_verification_email(recipient_email, recipient_name, ip,):
    # Get the user's location based on IP address
    try:
        location_response = requests.get(f"https://ip.hackclub.com/ip/{ip}").json()
        print("1")
        city = location_response.get('city_name')
        print("2")
        country = location_response.get('country_name')
        print("3")
    except Exception as e:
        raise Exception(f"Failed to get location for IP {ip}: {e}")
    
    verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(f"Sending verification email to {recipient_email} with code: {verification_code}")

    email = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div class="container mx-auto m-5 mt-10 bg-slate-800">
                <h1>
                    Reset Password
                </h1>
                <h3>
                    We have received a request to reset your password from the ip address {ip} at {city} in the country {country}. Please use the code below to reset your password:
                </h3>
                <div style="padding: 2px; padding-left: 12px; padding-right: 4px; background-color: #374151; border-radius: 8px; color: #cbd5e1;">
                    <p><strong>{verification_code}</strong></p>
                </div>
                <p>
                    If you did not request this, you can safely ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": f"{sender_email}",
                                    "Name": f"{sender_name}"
                            },
                            "To": [
                                    {
                                            "Email": f"{recipient_email}",
                                            "Name": f"{recipient_name}"
                                    }
                            ],
                            "Subject": "Password Reset",
                            "TextPart": "Here is your password code.",
                            "HTMLPart": f"{email}",
                    }
            ]
    }
    try:
        result = mailjet.send.create(data=data)
        return result, verification_code
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise Exception(f"Failed to send email: {e}")
'''
















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

        rows = cursor.execute("SELECT id, username, pw_hash FROM users WHERE username = ?", (username,)).fetchall()
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
        if session.get("step") != 2:
            return render_template('register.html')
        else:
            return render_template('register.html', step=2)
    else:
        if session.get("step") != 2:
            # Handle the registration form submission
            if not request.form.get("email"):
                return render_template('register.html', error="Missing email.")
            if not request.form.get("username"):
                return render_template('register.html', error="Missing username.")
            if not request.form.get("password"):
                return render_template('register.html', error="Missing password.")
            if not request.form.get("confirm_password"):
                return render_template('register.html', error="Missing confirm password.")

            email = request.form.get('email')
            if re.match("^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9-.]{2,25}$", email) is None:
                return render_template('register.html', error="Invalid email address.")
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if password != confirm_password:
                return render_template('register.html', error="Passwords do not match.")

            try:
                db = sqlite3.connect(db_path)
                cursor = db.cursor()
                rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
                db.close()
            except sqlite3.Error as e:
                return render_template('register.html', error=f"Database error: {e}")
            
            if len(rows) > 0:
                return render_template('register.html', error=f"Account with username '{username}' already exists.")
            
            pw_hash = generate_password_hash(password)

            try:
                # Insert the new user into the database
                # Change this to add to a cache which will be transferred to the database after verification
                db = sqlite3.connect(db_path)
                cursor = db.cursor()
                cursor.execute("INSERT INTO users (email, username, pw_hash) VALUES (?, ?, ?)", (email, username, pw_hash))
                db.commit()
                db.close()
            
                db = sqlite3.connect(db_path)
                cursor = db.cursor()
                rows = cursor.execute("SELECT id, pw_hash FROM users WHERE username = ?", (username,)).fetchall()
                db.close()
            except sqlite3.Error as e:
                return render_template('register.html', error=f"Database error: {e}")
            

            if len(rows) == 0:
                return render_template('register.html', error="Failed to create account. Please try again.")
            
            user = rows[0]
            user_id = user[0]
            password = user[1]
            session['user_id'] = user_id

            # Get the user's IP address
            try:
                if 'X-Forwarded-For' in request.headers:
                    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
                else:
                    ip = request.remote_addr
            except Exception as e:
                return render_template('register.html', error=f"Failed to get IP address: {e}")



            try:
                response, code = send_verification_email(email, username, ip)
            except Exception as e:
                return render_template('register.html', error=f"Failed to send verification email: {e}")
            
            if not response or response.status_code != 200:
                return render_template('register.html', error="Failed to send verification email. Please try again later.")
            
            # Store the verification code in the session
            session['verification_code'] = code


            session['step'] = 2
            return render_template('register.html', step=2)
        else:
            if not request.form.get("verification_code"):
                return render_template('register.html', step=2, error="Missing verification code.")
            session.pop('step', None)
            verification_code = request.form.get('verification_code')
            """
            if 'verification_code' not in session or session['verification_code'] != verification_code:
                return render_template('register.html', step=2, error=f"Incorrect verification code {verification_code}.")
            return render_template('dashboard.html', logged_in=True, error=f"This is the verification code {verification_code}. Correct.")
            """
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

# Leaderboard of most money lost
@app.route('/leaderboard')
def leaderboard():
    """
    if request.cookies.get('session') is None:
        return redirect('/')
    """
    today = str(datetime.date.today())
    
    try:
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        db_rows = cursor.execute(f"SELECT user_id, money_lost FROM leaderboard WHERE date = ? ORDER BY money_lost DESC", (today,)).fetchall()
        db.close()
        if len(db_rows) < 1:
            return render_template('leaderboard.html', logged_in=True, leaderboard_message="No entries in leaderboard.")

        leaderboard_rows = []
        for row in db_rows:
            user_id = row[0]
            db = sqlite3.connect(db_path)
            cursor = db.cursor()
            user_row = cursor.execute(f"SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
            db.close()
            username = user_row[0]
            money_lost = row[1]
            percent_money_lost = str((money_lost / start_capital) * 100) + "%"
            built_row = {
                'username': username,
                'money_lost': money_lost,
                'percent_money_lost': percent_money_lost
            }
            leaderboard_rows.append(built_row)
        if len(leaderboard_rows) < 1:
            return render_template('leaderboard.html', logged_in=True, error="No entries in leaderboard.")
    except Exception as e: # Change this to the specific sqlite exception:
        return render_template('leaderboard.html', logged_in=True, error=f"Error getting leaderboard: {e}")
    return render_template('leaderboard.html', logged_in=True, leaderboard=leaderboard_rows)

@app.route('/watchlist')
def watchlist():
    if request.cookies.get('session') is None:
        return redirect('/')
    return render_template('watchlist.html', logged_in=True)



# Account and settings
@app.route('/account')
def account():
    if request.cookies.get('session') is None:
        return redirect('/')
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    
    try:
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        user_row = cursor.execute("SELECT email, username FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        
        if not user_row:
            return render_template('account.html', logged_in=True, error="User not found.")
        
        email, username = user_row
    except sqlite3.Error as e:
        return render_template('account.html', logged_in=True, error=f"Database error: {e}")
    
    return render_template('account.html', logged_in=True, email=email, username=username)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if not request.cookies.get('session'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('reset-password.html', logged_in=True)
    else:
        return render_template('reset-password.html', logged_in=True, error="This feature is not implemented yet.")

@app.route('/change-username', methods=['GET', 'POST'])
def change_username():
    if not request.cookies.get('session'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('change-username.html', logged_in=True)
    else:
        if not request.form.get("new_username"):
            return render_template('change-username.html', logged_in=True, error="Missing new username.")
        
        new_username = request.form.get('new_username')
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect('/')
        
        return render_template('change-username.html', logged_in=True, error=f"new username: {new_username}.")

@app.route('/change-email', methods=['GET', 'POST'])
def change_email():
    if not request.cookies.get('session'):
        return redirect('/')
    if request.method == 'GET':
        return render_template('change-email.html', logged_in=True)
    else:
        if not request.form.get("new_email"):
            return render_template('change-email.html', logged_in=True, error="Missing new email.")
        
        new_email = request.form.get('new_email')
        user_id = session.get('user_id')
        
        if not user_id:
            return redirect('/')
        
        return render_template('change-email.html', logged_in=True, error=f"new email: {new_email}.")




@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico')

@app.route('/<path:unknown_path>')
def unknown_path(unknown_path):
    if request.cookies.get('session'):
        return render_template('404.html', path=unknown_path, logged_in=True), 404
    return render_template('404.html', path=unknown_path), 404






















if __name__ == '__main__':
    app.run(debug=debug, port=os.getenv("PORT"))