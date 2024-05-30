from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/start')
def home():
    return render_template('home.html')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=request.form.get('remember'))
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
