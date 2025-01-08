from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'kereta'  # Replace with your database name

mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")  # Simple query to test the connection
        cur.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)