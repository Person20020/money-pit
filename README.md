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
    username TEXT,
    pw_hash TEXT,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);
CREATE UNIQUE INDEX username ON users (username);
```