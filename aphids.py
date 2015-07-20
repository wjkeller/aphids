#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#     |  ..  |
#     |  ()  |
#     \  /\  /
#   /\ \/  \/ /\
#  /  \/    \/  \
# /   (aphids)   \
#     /\    /\ 
#    /  \__/  \
#    |a python|
#    |identity|
#    | server |

"""
aphids.py - A PytHon IDntity Server

Usage from the command line:

    pyvenv venv
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python aphids.py
"""

import itertools

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext import wtf
from passlib.context import CryptContext
import wtforms
from wtforms import validators

app = flask.Flask('aphids')
app.debug = True
app.secret_key = 'insecure dev key'
db = SQLAlchemy(app)
manager = Manager(app)
pw_context = CryptContext(schemes=['pbkdf2_sha512'])


class User(db.Model):
    """
    End user with login credentials
    """

    __tablename__ = 'aphids_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    pw_hash = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.pw_hash = pw_context.encrypt(password)

    def valid_password(self, password):
        return pw_context.verify(password, self.pw_hash)


class AuthenticateForm(wtf.Form):

    FORM_ERRORS = object()

    username = wtforms.TextField(
            'username',
            validators=[validators.Required('all fields required')],
    )
    password = wtforms.PasswordField(
            'password',
            validators=[validators.Required('all fields required')],
    )

    def validate(self):
        self.user = None
        valid = super().validate()
        if valid:
            self.user = User.query.filter_by(username=self.username.data).first()
            if self.user is None or not self.user.valid_password(self.password.data):
                self.errors.setdefault(self.FORM_ERRORS, []).append('invalid credentials')
                valid = False
        return valid


class RegisterForm(wtf.Form):

    username = wtforms.TextField(
        'username',
        validators=[validators.Required('all fields required')],
    )
    password = wtforms.PasswordField(
        'password',
        validators=[validators.Required('all fields required')],
    )
    confirm_password = wtforms.PasswordField(
        'confirm password',
        validators=[validators.EqualTo('password', 'password mismatch')],
    )


@app.route('/')
def welcome():
    return flask.render_template('welcome.html')


@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    form = AuthenticateForm()
    if form.validate_on_submit():
        return '{}'.format(form.user)
    return flask.render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return '{}'.format(user)
    return flask.render_template('register.html', form=form)


@app.route('/status')
def status():
    return flask.jsonify(status='ok')


@app.route('/version')
def version():
    return flask.jsonify(version='0.1.0')


if __name__ == '__main__':
    app.before_first_request(db.create_all)
    manager.run()
