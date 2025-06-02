# Money Pit

This is a game based on paper trading where the goal is to loose your money as fast as possible.


# Running
Here is how you can run the site yourself:

First clone the repo. Then create a python venv using `python -m venv venv`, activate the venv using `. venv/bin/activate`, and install libraries using `pip install -r requirements.txt`. Install npm packages using `npm install`.


## Database
The app uses a sqlite database. It has this schema to create it manually or can be automatically created using the `setup.sh` script:
```
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email TEXT,
    username TEXT,
    pw_hash TEXT,
    cash NUMERIC NOT NULL DEFAULT 1000000.00
);
CREATE TABLE signup_cache (
    id INTEGER PRIMARY KEY NOT NULL,
    email TEXT,
    username TEXT,
    pw_hash TEXT,
    verification_code TEXT,
    expiration DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE leaderboard (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER,
    money_lost NUMERIC,
    date TEXT
);

CREATE UNIQUE INDEX username ON users (username);
```