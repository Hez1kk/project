from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = '123'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    debts = db.relationship('Debt', backref='user', lazy=True)

class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    debt_type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'], endpoint='login_page')
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'ae0888sn' and password == 'ae0888sn':
            user = User.query.filter_by(name=username, is_admin=True).first()
            if not user:
                user = User(name=username, is_admin=True)
                db.session.add(user)
                db.session.commit()

            session['user_id'] = user.id
            return redirect(url_for('controlpanel'))
        else:
            return render_template('login.html', error="Authentication failed")

    return render_template('login.html')

@app.route('/controlpanel', methods=['GET', 'POST'])
def controlpanel():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user.is_admin:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        username = request.form['username']
        new_user = User(name=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('controlpanel'))

    users = User.query.all()
    return render_template('controlpanel.html', users=users)

@app.route('/add_debt', methods=['POST'])
def add_debt():
    user_id = session.get('user_id')
    debt_type = request.form['debt_type']
    amount = request.form['amount']

    if user_id:
        user = User.query.get(user_id)
        if user:
            new_debt = Debt(user_id=user_id, debt_type=debt_type, amount=amount)
            db.session.add(new_debt)
            db.session.commit()

    return redirect(url_for('user_debts'))

@app.route('/update_debt', methods=['POST'])
def update_debt():
    user_id = session.get('user_id')
    debt_id = request.form.get('debt_id')

    if debt_id is None:
        return redirect(request.referrer)

    new_amount = request.form['amount']

    if user_id:
        debt = Debt.query.get(debt_id)
        if debt and debt.user_id == user_id:
            debt.amount = new_amount
            db.session.commit()
            return redirect(url_for('user_debts'))
        else:
            return redirect(url_for('login_page'))



@app.route('/delete_debt', methods=['POST'])
def delete_debt():
    debt_id = request.form.get('debt_id')
    debt_to_delete = Debt.query.get(debt_id)
    if debt_to_delete:
        db.session.delete(debt_to_delete)
        db.session.commit()
    return redirect(url_for('user_debts'))

@app.route('/user_debts')
def user_debts():
    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            debts = user.debts
            return render_template('user_debts.html', user=user, debts=debts)

    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
