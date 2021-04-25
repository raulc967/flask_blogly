"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Posts, PostTag, Tag

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

@app.route('/<user>/posts')
def user_posts(user):
    posts = Posts.query.filter(Posts.user_id == user)
    return render_template('posts.html', posts=posts)

@app.route('/<user>/post/edit/<post_id>')
def edit_post(user, post_id):
    post = Posts.query.filter(Posts.id == post_id)
    return render_template('editPost.html', post=post, user=user)

@app.route('/<user>/post/edit/<post_id>', methods=['POST'])
def change_post(user, post_id):
    post = Posts.query.get(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    db.session.add(post)
    db.session.commit()
    return redirect(f'/{user}/posts')

@app.route('/<user>/post/delete/<post_id>', methods=['POST'])
def delete_post(user, post_id):
    post = Posts.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/{user}/posts')

@app.route('/<user>/post/<post_id>')
def ind_post(user, post_id):
    post = Posts.query.filter(Posts.id == post_id)
    user = User.query.filter(User.id == user)
    return render_template('post.html', post=post, user=user)

@app.route('/<user>/create_post')
def create_post(user):
    return render_template('createPosts.html', user=user)

@app.route('/<user>/create_post', methods = ['POST'])
def create_posts(user):
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = user
    post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/{user}/posts')

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

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<tag_id>')
def single_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/new')
def create_tag():
    return render_template('createTag.html')

@app.route('/tags/new', methods = ['POST'])
def create_tag_post():
    name = Tag(name = request.form.get('name'))
    db.session.add(name)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('editTag.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods = ['POST'])
def edit_tag_post(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form.get('name')
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')