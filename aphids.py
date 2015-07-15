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

app = flask.Flask('aphids')
app.debug = True


if __name__ == '__main__':
    app.run()
