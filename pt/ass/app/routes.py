from app import app
from app.forms import UserAdd, UserLogin, UserEdit
from flask import render_template, url_for, flash, redirect, request, session
from dbcon import DbConn
import gc
from passlib.hash import sha256_crypt

db_conn = DbConn()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Hello, Karl')


@app.route('/user_add', methods=['GET', 'POST'])
def user_add():
    form = UserAdd()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt((str(form.password.data)))
        flash('Hello, {}'.format(form.username.data))
        x = db_conn.sell(username, email)
        if int(x) > 0:
            flash('That username or email: {} is already taken, please choose another'.format(username))
            return render_template('user_add.html', form=form)
        else:
            db_conn.inss(username, password, email)
            db_conn.conn.commit()
            flash('Thank you for registration')
            db_conn.curser.close()
            db_conn.conn.close()
            session.pop('logged_in', None)
            session.clear()
            gc.collect()
            return redirect(url_for('index'))
    return render_template('user_add.html', title='Add User', form=form)


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    form = UserLogin()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        if request.method == 'POST':
            data = db_conn.log_p(username)
            data = db_conn.curser.fetchone()[2]
            if sha256_crypt.verify(password, data):
                session['logged_in'] = True
                session['username'] = username
                flash('Hi - {}'.format(username))
                return redirect(url_for('index'))

            else:
                flash('invalid password')

        return render_template('login_page.html', form=form)

    return render_template('login_page.html', title='Login', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit_page():
    flash('changed {}'.format(session))
    form = UserEdit()
    username = form.username.data
    username_ses = session['username']
    if request.method == "POST":
        data = db_conn.upd(username, username_ses)

        db_conn.conn.commit()
        db_conn.curser.close()
        db_conn.conn.close()
        flash('changed {}'.format(session))
    return render_template('edit.html', title='Edit_user', form=form)


@app.route("/delete")
def delete_data():
    username = session['username']
    db_conn.dlte(username)
    flash('Data <{}> deleted  successfully '.format(session['username']))
    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.clear()
    flash('You have been logged out.')
    gc.collect()
    return redirect(url_for('index'))
