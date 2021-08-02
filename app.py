from flask import Flask
from flask import render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask import session, request, g 
import os
import csv
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        with open('id.csv',"a+", newline='') as records:
            recordsSignUp = csv.writer(records)
            recordsSignUp.writerow([form.username.data, form.password.data])
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user',None)
    form = LoginForm()
    if form.validate_on_submit():
        with open('id.csv',"r") as records:
            recordsLogin = csv.reader(records)
            for row in recordsLogin:
                if form.username.data == row[0] and form.password.data == row[1]:
                    session['user'] = form.username.data
                    return redirect(url_for('todoList'))
        
    return  render_template('login.html', form=form)

@app.route('/todoList')
def todoList():
    if g.user:
        return  render_template('todoList.html')
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))
