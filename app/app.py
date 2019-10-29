from flask import Flask, flash, request, render_template, redirect, session, url_for
from datetime import timedelta
from app.forms import LoginForm

flask_app = Flask(__name__)
flask_app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

from app.models import db, User
from flask_login import LoginManager, login_user, login_required, logout_user

login_manager = LoginManager()
login_manager.init_app(flask_app)

import app.theft_e
import app.theft_r

@flask_app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

#@flask_app.route('/')
#def index():
#    return "Welcome to Flask"

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
#                    return "User logged in"
#                    flash("You're now logged in!")
                    print("Login success")
                    return(render_template('gates-selection.html'))
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

@login_manager.unauthorized_handler
def unauthorized():
    return("back to a login page")


@flask_app.route("/logout")
@login_required
def logout():
    logout_user()
    return(render_template("logout.html"))


@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


def init_db():
    db.init_app(flask_app)
    db.app = flask_app
    db.create_all()


@flask_app.route("/store-selection")
def store():
    return(render_template("page-2.html"))


@flask_app.route("/gates-selection")
@login_required
def gates_selection():
    return(render_template("gates-selection.html"))


@flask_app.route("/monitoring-exit")
@login_required
def monitoring():
    pics = app.theft_e.get_pic()
    return(render_template("monitoring.html", pics=pics))


@flask_app.route("/monitoring-restroom")
@login_required
def monitoring_2():
    pics = app.theft_r.get_pic()
    return(render_template("monitoring.html", pics=pics))
