from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = '123'

db = SQLAlchemy(app)

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class MyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    name = Name.query.all()
    return render_template('index.html', names=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == '123':
            return redirect(url_for('controlpanel'))
    return render_template('login.html')

@app.route('/controlpanel', methods=['GET', 'POST'])
def controlpanel():
    if request.method == 'POST':
        name = request.form['name']
        new_name = name(name=name)
        db.session.add(new_name)
        db.session.commit()
        return redirect(url_for('controlpanel'))
    names = Name.query.all()
    return render_template('controlpanel.html', names=names)

@app.route('/add_value', methods=['POST'])
def add_value():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        new_value = MyValue(Name=name, value=value)
        db.session.add(new_value)
        db.session.commit()
        return redirect(url_for('controlpanel'))

if __name__ == '__main__':
    app.run(debug=True)
