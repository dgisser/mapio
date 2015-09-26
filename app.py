from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/login')
def loginScreen():
	return render_template('login.html')

if __name__ == "__main__":
    app.run()
