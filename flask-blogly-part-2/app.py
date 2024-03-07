"""Blogly application."""

from flask import Flask, session, request, render_template, make_response, redirect, flash, url_for, abort

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']="yobananaboy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def list_of_users():
    users= User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('new_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
    # Get user input from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    # Create a new user instance
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Redirect to the /users route after adding a user
    flash('User added successfully!', 'success')
    return redirect('/users')


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
def user_details(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Get the post content from the form
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')

        # Create a new post
        new_post = Post(title=post_title, content=post_content)

        # Add the post to the user's posts
        user.posts.append(new_post)

        # Save changes to the database
        db.session.commit()

    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    # Get the updated user details from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    flash('User updated successfully!', 'success')
    return redirect(url_for('user_details', user_id=user.id))

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Your delete logic here
    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('list_of_users'))


@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    # Your delete logic here
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('user_details', user_id=user.id))



@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)



@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['GET'])
def show_post_details(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', user=user, post=post)

# app.py

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        # Get the updated post details from the form
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')

        # Update the post details
        post.title = post_title
        post.content = post_content

        # Save changes to the database
        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('user_details', user_id=user.id))

    return render_template('edit_post.html', user=user, post=post)
