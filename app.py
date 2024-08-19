from flask import Flask, render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def show_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('books.html', books=books)

@app.route('/users')
def show_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)


# Route to display the form and add a new book
@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
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

if __name__ == '__main__':
    app.run(debug=True)
