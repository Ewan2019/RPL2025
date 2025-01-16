from flask import Flask, render_template, request, url_for, flash, session, redirect
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


app = Flask(__name__)
app.secret_key = 'kuatkuat'  # Ganti dengan kunci rahasia yang SANGAT kuat dan acak!

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kereta'

mysql = MySQL(app)

@app.route('/')
def indeks():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/choice_regis')
def choice_regis():
    return render_template('choice-regis.html')


#registrasi  # Dekorator untuk route '/registrasi' (halaman registrasi)
@app.route('/regis_user', methods=('GET','POST'))
def regis_user():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        username = request.form['username']  # Mengambil username dari form
        email = request.form['email']  # Mengambil email dari form
        password = request.form['password']  # Mengambil password dari form

        #cek username atau email  # Memeriksa apakah username atau email sudah ada di database
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username, email, ))  # Menjalankan query untuk mencari username atau email
        akun = cursor.fetchone()  # Mengambil data akun yang ditemukan
        if akun is None:  # Jika akun tidak ditemukan
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, email, generate_password_hash(password)))  # Menjalankan query untuk memasukkan data akun baru
            mysql.connection.commit()  # Melakukan commit perubahan ke database
            flash('Registrasi Berhasil', 'success')  # Menampilkan pesan flash 'Registrasi Berhasil' dengan kategori 'success'
        else:  # Jika akun ditemukan
            flash('Username atau email sudah ada', 'danger')  # Menampilkan pesan flash 'Username atau email sudah ada' dengan kategori 'danger'
    return render_template('regis-user.html')  # Merender template 'registrasi.html'

@app.route('/regis_admin', methods=['GET', 'POST'])
def regis_admin():
    if request.method == 'POST':
        # Periksa apakah semua field yang diperlukan ada
        if 'username' not in request.form or 'email' not in request.form or 'password' not in request.form or 'admin_key' not in request.form:
            flash('Semua field harus diisi', 'danger')
            return render_template('regis-admin.html')
            
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        admin_key = request.form['admin_key']
        
        # Validasi input tidak boleh kosong
        if not username or not email or not password or not admin_key:
            flash('Semua field harus diisi', 'danger')
            return render_template('regis-admin.html')

        cursor = mysql.connection.cursor()
        try:
            # Cek username atau email
            cursor.execute('SELECT * FROM admin WHERE username=%s OR email=%s', (username, email))
            akun = cursor.fetchone()
            
            if akun is None:
                # Perbaiki placeholder $s menjadi %s
                cursor.execute('INSERT INTO admin VALUES (NULL, %s, %s, %s, %s)', 
                             (username, email, generate_password_hash(password), admin_key))
                mysql.connection.commit()
                flash('Registrasi Berhasil', 'success')
                return redirect(url_for('login'))  # Redirect ke halaman login setelah berhasil
            else:
                flash('Username atau email sudah ada', 'danger')
                
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        finally:
            cursor.close()
            
    return render_template('regis-admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        try:
            # Cek di tabel admin terlebih dahulu
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
            admin = cursor.fetchone()
            
            if admin and check_password_hash(admin[3], password):  
                session['loggedin'] = True
                session['id'] = admin[0]  
                session['username'] = admin[1]  
                session['is_admin'] = True
                return redirect(url_for('admin_dashboard'))  
            
            # Jika bukan admin, cek di tabel users
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[3], password):  
                session['loggedin'] = True
                session['id'] = user[0]  
                session['username'] = user[1]  
                session['is_admin'] = False
                return redirect(url_for('indeks'))  
            
            flash('Username atau password salah', 'danger')
                
        except mysql.connector.Error as e:
            flash(f'Error database: {e}', 'danger')
        finally:
            cursor.close()
            
    return render_template('login.html')

# Decorator untuk proteksi route admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin') or not session.get('is_admin'):
            flash('Anda harus login sebagai admin', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator untuk proteksi route user biasa
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin'):
            flash('Silakan login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/user_view')
@login_required  # Menambahkan proteksi
def user_view():
    return render_template('user-view.html')

@app.route('/admin_view')
@admin_required  # Menambahkan proteksi
def admin_view():
    return render_template('admin-view.html')



if __name__ == '__main__':
    app.run(debug=True)