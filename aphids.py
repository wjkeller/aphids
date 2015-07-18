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

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from passlib.context import CryptContext

app = flask.Flask('aphids')
app.debug = True
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

    def set_password(self, password):
        self.pw_hash = pw_context.encrypt(password)

    def valid_password(self, password):
        return pw_context.verify(password, self.pw_hash)


@app.route('/')
def welcome():
    return flask.render_template('welcome.html')


if __name__ == '__main__':
    manager.run()
