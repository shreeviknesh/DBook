from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo

from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'dbook'
app.config['MONGO_URI'] = 'mongodb://shree:strongpassword123@ds060369.mlab.com:60369/dbook'
app.config['SECRET_KEY'] = '97542ec161edf850af891551159ea600'
mongo = PyMongo(app)

@app.route('/')
def index_route():
    if 'username' in session:
        flash(f'Logged in as {session["username"]}','info')
        return redirect(url_for('profile_route'))
    return render_template('index.html', align_center=True)

@app.route('/register', methods = ['GET', 'POST'])
def register_route():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('profile_route'))
    return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login_route():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in as {form.username.data}!', 'success')
        return redirect(url_for('index_route'))
    return render_template('login.html', form=form)

@app.route('/profile')
def profile_route():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)