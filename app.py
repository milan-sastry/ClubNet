from sys import path
path.append('src')  #go to src directory to import
from flask import Flask, render_template, redirect
from CASClient import CASClient
import secrets

# app info
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def hello():
    return render_template('initial.html')

@app.route('/application')
def application():
    netid = CASClient().Authenticate()
    return render_template('inside.html', CASValue = netid)

if __name__ == '__main__':
    app.run(host='localhost', port=5555)
