aphids - A PytHon IDentity Server
=================================

A simple identity server in python using [Flask][] and [SQLAlchemy][].

[Flask]: http://flask.pocoo.org/
[SQLAlchemy]: http://www.sqlalchemy.org/


Development
-----------

Currently developing on python 3.4.

Setup:

```
$ pyvenv venv
$ ./venv/bin/pip install -r requirements.txt
```

Run:

```
$ ./venv/bin/python aphids.py
```

Test:

```
$ ./venv/bin/pip install pytest lxml cssselect
$ ./venv/bin/py.test test_aphids.py
```
