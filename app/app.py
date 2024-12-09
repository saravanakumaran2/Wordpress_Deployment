from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database connection details
db_config = {
    'host': 'mysql-server',  # This is the name of the MySQL container
    'user': 'root',
    'password': 'root',
    'database': 'users'
}

def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# Call this function before running the app
create_table()


# Function to create MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        return connection
    else:
        raise Exception("Database connection failed")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return redirect(url_for('home'))  # Redirect to home page if credentials are correct
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (new_username, new_password))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
