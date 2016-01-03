from flask import Flask, render_template, flash, request, url_for, redirect, session, Markup, escape
from jinja2 import Markup as Mkup
import time
import datetime
from content_management import Content
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.fields import StringField
from wtforms.widgets import TextArea
from functools import wraps
from passlib.hash import sha256_crypt
from python_mysql_dbconfig import read_db_config
from mysql.connector import MySQLConnection, Error
import gc





TOPIC_DICT = Content()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Blog'

db = SQLAlchemy()
db.init_app(app)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])


class PostForm(Form):
    post = StringField('', widget=TextArea(), validators=[validators.Length(min=4, max=1023)]) 




@app.route("/")
@app.route("/<int:var>/")
def blog(var=0):
    gc.collect()
    try:
        entry = []
        if var == 0:
            for x in range(len(TOPIC_DICT['Blog'])/(len(TOPIC_DICT['Blog'])/2)):
                entry.append(TOPIC_DICT['Blog'][var+x])
            prev = -1
        else:
            for x in range(len(TOPIC_DICT['Blog'])/(len(TOPIC_DICT['Blog'])/2)):
                if (var*2)+x <= len(TOPIC_DICT['Blog']) -1:
                    entry.append(TOPIC_DICT['Blog'][(var*2)+x])
            prev = var - 1

        var += 1 

        if var*2 == len(TOPIC_DICT['Blog']):
            var = 0
            label = 'Back to Beginning'
        else:
            label = 'Next'

        return render_template("blog.html", entry=entry, next = var, prev = prev, label = label, TOPIC_DICT = TOPIC_DICT)
    except Exception as e:
        return render_template("error.html", error='An error occured. Please refresh.')



@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'



@app.route("/bio/")
def bio():
    try:
        return render_template("bio.html")
    except Exception as e:
        return render_template("error.html", error='An error occured. Please refresh.')



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You must log in first!")
            return redirect(url_for('login_page'))
    return wrap


def already_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in  session:
            flash("You are already logged in!")
            return redirect(url_for('blog'))
        else:
            return f(*args, **kwargs)
    return wrap


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("Goodbye!")
    gc.collect()
    return redirect(url_for('blog'))



@app.route("/login/", methods = ['GET','POST'])
@already_logged_in
def login_page():
    error = ''
    gc.collect()
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cur = conn.cursor()
        if request.method == "POST":
            query = ("""SELECT * FROM users WHERE username = %s""")
            cur.execute(query, (request.form['username'],))
            userpw = cur.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], userpw):
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['user-ip'] = request.remote_addr
                if session['username'] == 'admin':
                    flash(Markup('The Dark Knight&nbsp;&nbsp;<span class="glyphicon glyphicon-knight"></span>'))
                else:
                    flash('Logged In')
                return redirect(url_for('blog'))
            else:
                error = "Invalid Credentials. Please try again."

        gc.collect()

        return render_template('login.html', error = error)

    except Exception as e:
        error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error = error)


@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cur = conn.cursor()

            query = ("""SELECT * FROM users WHERE username = %s""")
            cur.execute(query, (username,))

            row = cur.fetchone()

            if row:
                flash("That username has already been used. Please try another")
                return render_template ('register.html', form = form)
            else:
                try:
                    url = '/about/'
                    query = ("INSERT INTO users(username, email, password, tracking)"
                        "VALUES (%s,%s,%s,%s)")
                    cur.execute(query,(username, email, password, url))

                    conn.commit()
                    
                    cur.close()
                    conn.close()
                    gc.collect()
                    
                    session['logged_in'] = True
                    session['username'] = username

                    flash('Success')

                    return redirect(url_for('blog'))
                except Exception as e:
                    return render_template('error.html', error = 'Error occured. Please refresh')

        return render_template("register.html", form=form)

    except Exception as e:
        return render_template('error.html', error = 'An error occured. Please refresh.')
        




@app.route("/blog/<path:path>/", methods = ['GET', 'POST'])
def route_to_blogs(path=''):
    try:
        for blog in TOPIC_DICT['Blog']:
            if str(path) == str(blog[1].replace('/','')):
                return redirect(path)
        return page_not_found('404: Page not found')
    except Exception as e:
        return render_template('error.html', error = 'An error occured. Please refresh.')




@app.route("/<path:path>/", methods = ['GET', 'POST'])
def blog_routes(path=''):
    try:
        for x in range(len(TOPIC_DICT['Blog'])):
            if str(path) == str(TOPIC_DICT['Blog'][x][1].replace('/','')):
                try:
                    form = PostForm(request.form)

                    curLink = TOPIC_DICT['Blog'][x][1]
                    curTitle = TOPIC_DICT['Blog'][x][0]
                    curPost = TOPIC_DICT['Blog'][x][2]
                    curCode = TOPIC_DICT['Blog'][x][3]
                    curExpl = TOPIC_DICT['Blog'][x][4]

                    if x == (len(TOPIC_DICT['Blog']) -1):
                        nextLink = TOPIC_DICT['Blog'][0][1]
                        nextTitle = TOPIC_DICT["Blog"][0][0]
                    else:
                        nextLink = TOPIC_DICT['Blog'][x+1][1]
                        nextTitle = TOPIC_DICT["Blog"][x+1][0]

                    if x == 0:
                        prevLink = TOPIC_DICT["Blog"][-1][1]
                    else:
                        prevLink = TOPIC_DICT["Blog"][x-1][1]

                    url = TOPIC_DICT['Blog'][x][1]
                    dbconfig = read_db_config()
                    conn = MySQLConnection(**dbconfig)
                    cur = conn.cursor()
                    query = ("""SELECT u.username, p.post, p.submit_time FROM users u INNER JOIN posts p ON u.uid = p.uid WHERE p.blog_route = %s""")
                    cur.execute(query, (url,))
                    submitted_posts = cur.fetchall()



                    if request.method == "POST" and form.validate():
                        post = form.post.data
                        if post:
                            try:
                                url = TOPIC_DICT['Blog'][x][1]
                                query = ("""SELECT uid FROM users WHERE username = %s""")
                                cur.execute(query, (session['username'],))
                                uid = cur.fetchone()[0]

                                query = ("INSERT INTO posts(uid, post, blog_route)"
                                    "VALUES (%s,%s,%s)")

                                cur.execute(query,(uid, post, url))
                                
                                conn.commit()

                                cur.close()
                                conn.close()
                                gc.collect()
                                flash('Post Submitted!')
                                return redirect(url)
                            except Exception as e:
                                return render_template("error.html", error = 'An error occured. Please refresh.')

                    return render_template("Blog"+TOPIC_DICT['Blog'][x][1][:-1]+".html", form = form, submitted_posts = submitted_posts, curLink = curLink, curTitle = curTitle, curPost = curPost, curCode = curCode, curExpl = curExpl, nextLink = nextLink, nextTitle = nextTitle, prevLink = prevLink)            
                except Exception as e:
                    return render_template("error.html", error = 'An error occured. Please refresh.')
        return page_not_found('404: Page not found')
    except Exception as e:
        return render_template('error.html', error = 'An error occured. Please refresh.')


@app.route('/robots.txt/')
def robots():
    return("User-agent: *\nDisallow: /register/\nDisallow: /login/\nDisallow: /donation-success/")



@app.errorhandler(404)
def page_not_found(e):
		return render_template("error.html", error = e)

@app.errorhandler(500)
def internal_error(e):
		return render_template("error.html", error = e)
if __name__ == "__main__":
    app.run()