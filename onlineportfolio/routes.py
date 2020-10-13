import os
import secrets
import random
from flask import render_template, request, url_for, flash, redirect, send_from_directory
from onlineportfolio import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from onlineportfolio.forms import RegistrationForm, LoginForm, AddCVForm, AddAboutForm, DownloadCVForm
from onlineportfolio.models import User


@app.route('/', methods=['GET', 'POST'])
def index():
    downloadcvform = DownloadCVForm()

    if downloadcvform.validate_on_submit():
        me = User.query.first()
        cvfile = me.cv_file
        cvfiles = os.path.join(app.root_path, 'static/cvfiles')
        return send_from_directory(directory=cvfiles, filename=cvfile)

    return render_template("index.html", downloadcvform=downloadcvform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('edit'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


def save_cv(form_cv):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_cv.filename)
    cv_fn = random_hex + f_ext
    cv_path = os.path.join(app.root_path, 'static/cvfiles', cv_fn)
    form_cv.save(cv_path)

    return cv_fn


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    cvform = AddCVForm()
    aboutform = AddAboutForm()

    if cvform.validate_on_submit():
        if not current_user.cv_file:
            if cvform.cv_file.data:
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been uploaded', 'success')
        elif current_user.cv_file:
            if cvform.cv_file.data:
                cvfilename = current_user.cv_file
                path = os.path.join(
                    app.root_path, 'static/cvfiles', cvfilename)
                os.remove(path)
                cv = save_cv(cvform.cv_file.data)
                current_user.cv_file = cv
                db.session.commit()
                flash('Your CV has been uploaded', 'success')

    if aboutform.validate_on_submit():
        current_user.statement = aboutform.self_desc.data
        db.session.commit()
        flash('Profile updated', 'success')
    elif request.method == 'GET':
        if current_user.statement:
            aboutform.self_desc.data = current_user.statement

    return render_template("edit.html", cvform=cvform, aboutform=aboutform)
