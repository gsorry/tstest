# tstest

Simple REST API based app in Flask.

# Install

It is recommended to use the latest version of Python 3 and PyPy.

Clone the repository:
```shell script
git clone https://github.com/gsorry/tstest.git
cd tstest
```


Python 3 comes bundled with the `venv` module to create virtual environments.

Create a virtual environment:
```shell script
python3 -m venv venv
```

Before you work on your project, activate the corresponding environment:
```shell script
. venv/bin/activate
```

Within the activated environment, use the following command to install Flask:
```shell script
pip3 install -e .
```

## Run (Development only)

Now you can run your application using the `flask` command.
From the terminal, tell Flask where to find your application, then run it in development mode:
```shell script
export FLASK_APP=tsapp
export FLASK_ENV=development
flask init-db
flask run
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

## Test

```shell script
pip3 install '.[test]'
pytest
```

Run with coverage report:
```shell script
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```

## Build

Make sure the wheel library is installed first:
```shell script
pip3 install wheel
```

Build a wheel distribution file:
```shell script
python3 setup.py bdist_wheel
```

## Deploy

You can find the file in `dist/tsapp-1.0.0-pu2.py3-none-any.whl`.
The file name is the name of the project, the version, and some tags about the file can install.

Copy this file to another machine,
[set up a new virtualenv](https://flask.palletsprojects.com/en/1.1.x/installation/#install-create-env),
then install the file with pip:
```shell script
pip3 install tsapp-1.0.0-py2.py3-none-any.whl
```

Pip will install your project along with its dependencies.

When Flask detects that it’s installed (not in editable mode),
it uses a different directory for the instance folder.
You can find it at `venv/var/flaskr-instance` instead.

Create the `config.py` file in the instance folder, which the factory will read from if it exists.

`venv/var/tsapp-instance/config.py`:
```
SECRET_KEY='<RANDOM_SECRET_KEY>',
```

## Run with a Production Server

When running publicly rather than in development,
you should not use the built-in development server (`flask run`).

Instead, use a production WSGI server.
For example, to use Waitress, first install it in the virtual environment:
```shell script
pip3 install waitress
```

You need to tell Waitress about your application, but it doesn’t use FLASK_APP like flask run does.
You need to tell it to import and call the application factory to get an application object.

```shell script
waitress-serve --call 'tsapp:create_app'
```
