from flask import Flask, render_template,request,redirect,url_for, session, flash
import sqlite3
# from dotenv import load_dotenv
# import os
# Load environment variables from .env file
# load_dotenv()
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
# Raise an error in production if SECRET_KEY is not set
# if app.config['ENV'] == 'production' and not os.getenv('SECRET_KEY'):
#     raise RuntimeError("SECRET_KEY environment variable not set in production environment.")


def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username= session['username'])
    else:
        flash('You need to login first.', 'warning')
        return redirect(url_for('login'))

@app.route('/books', methods=('GET', 'POST'))
def show_books():
    # if 'username' not in session:
    #     return render_template('login.html')
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('books.html', books=books)

@app.route('/users')
def show_users():
    # if 'username' not in session:
    #     return render_template('login.html')
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)


# Route to display the form and add a new book
@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
#    if 'username' not in session:
#         return render_template('login.html')
   if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        published_year = request.form.get('published_year')
        isbn = request.form.get('isbn')
        copies = request.form.get('copies')
        if not title or not author or not published_year or not isbn or not copies:
            return "All fields are required!", 400
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, published_year, isbn, copies) VALUES (?, ?, ?, ?, ?)',
                     (title, author, published_year, isbn, copies))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))  # Redirect to the home page or any other page
   else:
        return render_template('add_book.html')
   
@app.route('/add_user', methods=('GET', 'POST'))
def add_user():
    # name TEXT NOT NULL,
    # email TEXT UNIQUE NOT NULL,
    # phone TEXT NOT NULL
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        if not name or not email or not phone:
            return "All fields are required!", 400
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email, phone) VALUES (?, ?, ?)',
                    (name, email, phone))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))  # Redirect to the home page or any other page
    else:
        return render_template('add_user.html')
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:
            return "All fields are required!", 400
        print(name)
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE name = ? AND email = ?', (name, email)).fetchone()
        conn.close()
        if user and user["email"] == email:
            session['username'] = user["name"]
            flash('Login successful!', 'success')
            print("User matched!")
            return redirect(url_for('dashboard'))
        else:
            return "Login failed: Incorrect name or email.", 401
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    else:
        flash('You need to log in first!', 'warning')
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
