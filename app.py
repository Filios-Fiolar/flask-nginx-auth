from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

open("users.db", "a").close()  # створюємо файл, якщо не існує

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_PATH = 'users.db'

# Ініціалізація бази, якщо ще не існує
if os.stat(DB_PATH).st_size == 0:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute("INSERT INTO users VALUES (?, ?)", ('test', '1234'))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Неправильний логін або пароль'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            error = 'Користувач уже існує'
        else:
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            session['username'] = username
            return redirect(url_for('home'))
        conn.close()
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8000)
