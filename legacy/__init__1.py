from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
# from dbconn import Connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from python_mysql_dbconfig import read_db_config
from mysql.connector MySQLConection, Error
import gc

TOPIC_DICT = Content()

app = Flask(__name__)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    

@app.route("/")
def homepage():
    return render_template("main.html")


@app.route("/dashboard/")
def dashboard():
	try:
		flash("Welcome")
		return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
	except Exception as e:
		return render_template("error.html", error=e)


@app.route("/login/", methods = ['GET','POST'])
def login_page():
	error = ''

	try:
		try:
		 	if request.method == "POST":
		 		attempted_username = request.form['username']
		 		attempted_password = request.form['password']

		 		if attempted_username == "admin" and attempted_password == "password":
		 			return redirect(url_for('dashboard'))
		 		else:
		 			error = "Invalid Credentials"
		 			
		 	return render_template('login.html', error = error)

		except Exception as e:
			return render_template("login.html", error = e)
	except Exception as e:
		return render_template('error.html', error = e)


@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            dbconfig = read_db_config()
            conn = MySQLConection(**dbconfig)
            cur = conn.cursor

            query = ("SELECT * FROM users "
                "WHERE username = '{0}'".format(username))
            
            cur.execute(query)

            row = cur.fetchone()

            if row:
                flash("That username has already been used. Please try another")
                return render_template ('register.html', form = form)
            else:
                url = '/about/'
                query = ("INSERT INTO users (username, email, password, tracking)"
                    "VALUES (%s,%s,%s,%s)")
                cur.execute(query,(username, email, password, url))
                conn.commit()
                
                cur.close()
                conn.close()
                gc.collect()
                
                session['logged_in'] = True
                session['user'] = username

                redirect(url_for('dashboard'))


        return render_template("register.html", form=form)

    except Exception as e:
        return render_template('error.html', error = e)
		


@app.errorhandler(404)
def page_not_found(e):
		return render_template("error.html", error = e)

@app.errorhandler(500)
def page_not_found(e):
		return render_template("error.html", error = e)
if __name__ == "__main__":
    app.run()
