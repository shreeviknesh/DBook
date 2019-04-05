from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import secrets

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

app.config['MONGO_DBNAME'] = 'dbook'
app.config['MONGO_URI'] = 'mongodb://shree:strongpassword123@ds060369.mlab.com:60369/dbook'
mongo = PyMongo(app)

@app.route('/')
def index_route():
    if 'username' in session:
        flash(f'Already logged in as {session["username"]}','info')
        return redirect(url_for('profile_route'))
    return render_template('index.html', align_center=True)

@app.route('/register', methods = ['GET', 'POST'])
def register_route():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form['username']
        existing_user = mongo.db.users.find_one({"username":username})

        if existing_user is None:
            password = request.form['password']
            email = request.form['email']

            mongo.db.users.insert_one({
                "username": username,
                "password": password,
                "email": email
            })

            session['username'] = username
            flash(f'User {username} created successfully!', 'success')
            return redirect(url_for('profile_route'))
        else:
            flash(f'Username {username} is already taken!', 'danger')
            return redirect(url_for('register_route'))

    return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = mongo.db.users.find_one({"username": username})

        if existing_user is None:
            flash('Invalid username/password', 'danger')
            return redirect(url_for('login_route'))

        if existing_user['password'] == password:
            flash(f'Logged in as {username}', 'success')
            return redirect(url_for('profile_route'))
        else:
            flash('Invalid username/password', 'danger')
            return redirect(url_for('login_route'))

    return render_template('login.html', form=form)

@app.route('/profile')
def profile_route():
    return render_template('profile.html')

@app.route('/logout')
def logout_route():
    #creating a new secret would clear all sessions
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index_route'))

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)