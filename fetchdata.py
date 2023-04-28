from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def display_users():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT name, age, email, mobile_number, education, gender, occupation, marital_status FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run()