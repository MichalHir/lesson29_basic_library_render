import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the 'books' table with an additional 'copies' field
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INTEGER NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    copies INTEGER NOT NULL
)
''')

# Create the 'users' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL
)
''')

# Create the 'loans' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    loan_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

# Insert sample data into the 'books' table with the 'copies' field
cursor.execute('''
INSERT INTO books (title, author, published_year, isbn, copies) VALUES
('1984', 'George Orwell', 1949, '1234567890123', 5)
''')
cursor.execute('''
INSERT INTO books (title, author, published_year, isbn, copies) VALUES
('To Kill a Mockingbird', 'Harper Lee', 1960, '1234567890124', 3)
''')
cursor.execute('''
INSERT INTO books (title, author, published_year, isbn, copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '1234567890125', 4)
''')

# Insert sample data into the 'users' table
cursor.execute('''
INSERT INTO users (name, email, phone) VALUES
('John Doe', 'john.doe@example.com', '555-1234')
''')
cursor.execute('''
INSERT INTO users (name, email, phone) VALUES
('Jane Smith', 'jane.smith@example.com', '555-5678')
''')
cursor.execute('''
INSERT INTO users (name, email, phone) VALUES
('Emily Johnson', 'emily.johnson@example.com', '555-8765')
''')

# Insert sample data into the 'loans' table
cursor.execute('''
INSERT INTO loans (book_id, user_id, loan_date, return_date) VALUES
(1, 1, '2024-08-01', '2024-08-15')
''')
cursor.execute('''
INSERT INTO loans (book_id, user_id, loan_date, return_date) VALUES
(2, 2, '2024-08-03', NULL)
''')
cursor.execute('''
INSERT INTO loans (book_id, user_id, loan_date, return_date) VALUES
(3, 3, '2024-08-05', '2024-08-12')
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully, and sample data inserted.")
