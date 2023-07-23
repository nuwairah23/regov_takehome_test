from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'regov_takehome_assignment'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'regov'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


def prep_connection():
    cur = mysql.connection.cursor()
    return cur


def terminate_db(cursor):
    cursor.close()


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = prep_connection()
        cursor.execute('''SELECT * FROM users WHERE email = %s AND password = %s''', (email, password))
        users = cursor.fetchone()
        terminate_db(cursor)

        if users:
            session['loggedin'] = True
            session['userid'] = users['userid']
            session['name'] = users['name']
            session['email'] = users['email']

            return render_template('userprofile.html')
        else:
            message = 'Oops! Incorrect credentials. The email or password you entered is incorrect.'

    return render_template('login.html', message=message)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()

    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']

        if username == '' or password == '' or email == '':
            message = 'Please complete the form before submitting!'

        else:
            cursor = prep_connection()

            cursor.execute('''SELECT * FROM users WHERE email = %s''', (email,))
            account = cursor.fetchone()

            if account:
                message = 'Account already exists!'
            else:
                cursor.execute('''INSERT INTO users VALUES (NULL, %s, %s, %s)''', (username, email, password))
                mysql.connection.commit()
                terminate_db(cursor)

                message = 'You have successfully registered!'

    return render_template('register.html', message=message)


if __name__ == "__main__":
    app.run()
