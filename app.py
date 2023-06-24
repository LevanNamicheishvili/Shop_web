from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = 'Hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# Api Fetch
@app.route('/')
def home():
    api_url = 'https://fakestoreapi.com/products?limit=10'
    response = requests.get(api_url)
    data = response.json()
    flash('Welcome to the Online Shop!', 'success')
    return render_template('home.html', products=data)


@app.route('/about')
def about():
    flash('This is the About page', 'info')
    return render_template('about.html')


@app.route('/products')
def products():
    flash('Browse our products', 'info')
    return render_template('products.html')


@app.route('/contact')
def contact():
    flash('Contact us for any inquiries', 'info')
    return render_template('contact.html')


@app.route('/faq')
def faq():
    flash('Frequently Asked Questions', 'info')
    return render_template('faq.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return f"Registration successful! Welcome, {username}."
    else:
        return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
