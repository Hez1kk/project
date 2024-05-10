from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = '123'

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class MyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

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
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('controlpanel'))
    items = Item.query.all()
    return render_template('controlpanel.html', items=items)

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
