from flask import Flask, render_template, request, url_for, flash, session, redirect
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

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

#registrasi  # Dekorator untuk route '/registrasi' (halaman registrasi)
@app.route('/regis_admin', methods=('GET','POST'))
def regis_admin():
    if request.method == 'POST':  # Memeriksa apakah metode request adalah POST
        username = request.form['username']  # Mengambil username dari form
        email = request.form['email']  # Mengambil email dari form
        password = request.form['password']  # Mengambil password dari form

        #cek username atau email  # Memeriksa apakah username atau email sudah ada di database
        cursor = mysql.connection.cursor()  # Membuat objek cursor untuk menjalankan query
        cursor.execute('SELECT * FROM tb_users WHERE username=%s OR email=%s', (username, email, ))  # Menjalankan query untuk mencari username atau email
        akun = cursor.fetchone()  # Mengambil data akun yang ditemukan
        if akun is None:  # Jika akun tidak ditemukan
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, email, generate_password_hash(password)))  # Menjalankan query untuk memasukkan data akun baru
            mysql.connection.commit()  # Melakukan commit perubahan ke database
            flash('Registrasi Berhasil', 'success')  # Menampilkan pesan flash 'Registrasi Berhasil' dengan kategori 'success'
        else:  # Jika akun ditemukan
            flash('Username atau email sudah ada', 'danger')  # Menampilkan pesan flash 'Username atau email sudah ada' dengan kategori 'danger'
    return render_template('regis-admin.html')  # Merender template 'registrasi.html'

@app.route('/login', methods=['GET', 'POST'])  # Definisikan route login
def login():
    if request.method == 'POST':
        # Logika login Anda di sini... (periksa username/password terhadap database)
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[3], password): # Pastikan indeks 3 adalah kolom password
                session['loggedin'] = True
                session['id'] = user[0] # Pastikan indeks 0 adalah ID pengguna
                session['username'] = user[1] # Pastikan indeks 1 adalah username
                return redirect(url_for('indeks'))
            else:
                flash('Username atau password salah', 'danger')
        except mysql.connector.Error as e:
            flash(f'Error database: {e}', 'danger')
        finally:
            cursor.close()
    return render_template('login.html')

@app.route('/user_view')
def user_view():
    return render_template('user-view.html')

@app.route('/admin_view')
def admin_view():
    return render_template('admin-view.html')



if __name__ == '__main__':
    app.run(debug=True)