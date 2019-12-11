from flask import Flask, flash, make_response, request, render_template, redirect, session, url_for
from datetime import timedelta
from app.forms import LoginForm
from werkzeug.security import check_password_hash
import logging

logging.basicConfig(filename='logs/log_in.log',level=logging.DEBUG)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

flask_app = Flask(__name__)
flask_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

from app.models import db, User
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(flask_app)

import app.theft_exit_p
import app.theft_exit_em
import app.theft_rest_p
import app.theft_rest_em

@flask_app.before_request
def before_request():
    session.permanent = True
    flask_app.permanent_session_lifetime = timedelta(minutes=720)

@flask_app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,post-check=0, pre-check=0'"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return(response)

@login_manager.unauthorized_handler
def unauthorized():
    return(render_template("index.html"))

@flask_app.route('/')
def index():
    return(render_template("index.html"))

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            password = request.form['password']
            email = request.form['email']
            if user:
                if user and check_password_hash(user.password, password):
                    session['email'] = email #saving the login for the session
                    print("PRINTING HERE {}".format(session['email']))
                    login_user(user)
#                    return "User logged in"
#                    flash("You're now logged in!")
                    print("Login success")
#                    logging.info('%s logged in successfully', user.email)
                    return(redirect(url_for('gates_selection')))
                else:
#                   return "Wrong password"
#                    flash("No user with that email/password combo")
                    print("login failed")
                    return(render_template('login.html', form=form))
            else:
                return "user doesn't exist"
    else:
        return "form not validated"

#@flask_app.route('/protected')
#@login_required
#def protected():
#    return("protected area")


@flask_app.route("/logout")
@login_required
def logout():
    logout_user()
#    return(render_template("logout.html"))
    return(redirect(url_for("login")))

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


def init_db():
    db.init_app(flask_app)
    db.app = flask_app
    db.create_all()


#@flask_app.route("/store-selection")
#def store():
#    return(render_template("page-2.html"))


@flask_app.route("/gates-selection")
@login_required
def gates_selection():
    return(render_template("gates-selection.html"))


@flask_app.route("/monitoring-exit")
@login_required
def monitoring():
    if session['email'] == 'lena':
        pics = app.theft_exit_p.get_pic()
        gates_info = "Entrance/Exit"
        return(render_template("monitoring.html", pics=pics, gates_info=gates_info))
    elif session['email'] == 'test':
        pics = app.theft_exit_em.get_pic()
        gates_info = "Entrance/Exit"
        return(render_template("monitoring.html", pics=pics, gates_info=gates_info))

@flask_app.route("/monitoring-restroom")
@login_required
def monitoring_2():
    if session['email'] == 'lena':
        gates_info = "Restroom"
        pics = app.theft_rest_p.get_pic()
        return(render_template("monitoring.html", pics=pics, gates_info=gates_info))
    elif session['email'] == 'test':
        gates_info = "Restroom"
        pics = app.theft_rest_em.get_pic()
        return(render_template("monitoring.html", pics=pics, gates_info=gates_info))
