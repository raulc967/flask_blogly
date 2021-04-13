"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mochii007@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """ This is the home route that will display all of the users in the database """

    users = User.query.all()
    return render_template('home.html', title='Blogly - Home', users=users)

@app.route('/<user>')
def user(user):
    """ This route will show the information of a specific user """

    user = User.query.get(user)
    return render_template('user.html', user=user)

@app.route('/create_user')
def create_user():
    """ This route will be used to display the form to create a new user """

    return render_template('createUser.html')

@app.route('/create_user', methods = ['POST'])
def create():
    """ This route is a POST method that actually updates the database to create the new user and redirects to the home page """

    first = request.form.get('first')
    last = request.form.get('last')
    url = request.form.get('url')
    user = User(first_name=first, last_name=last, image_url=url)
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/delete_user/<id>', methods=['POST'])
def delete(id):
    """ This route will be used to delete a user with a POST method """

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/update_user/<id>', methods=['POST'])
def update(id):
    """ This route will be used to update a user in the database """

    user = User.query.get(id)
    user.first_name = request.form.get('first')
    user.last_name = request.form.get('last')
    user.image_url = request.form.get('url')
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/update_user/<user>')
def update_page(user):
    """ This route will be used to show the form that will be used to update the user """
    
    user = User.query.get(user)
    return render_template('update.html', user=user)