from dotenv import load_dotenv
from flask import Flask, render_template, request
import os
import sqlite3


load_dotenv()
app = Flask(__name__)

db_path = os.getenv("DB_PATH")
if not db_path:
    raise ValueError("DB_PATH environment variable is not set.")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found at {db_path}.")
if not os.access(db_path, os.R_OK):
    raise PermissionError(f"Database file at {db_path} is not readable.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')