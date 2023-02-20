"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "my_blogly"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# Confused about why I need this, but it seemed to fix the issues I had with getting the app to run...
with app.app_context():
    # db.init_app(app)
    db.create_all()

@app.route('/')
def redirect_to_users():
    """Redirect to list of all users."""

    return redirect('/users')

@app.route('/users')
def show_users():
    """Show a list of all users. Each user is a link to their detail page. Also has link to form that adds a user."""
    
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def show_new_user_form():
    """Show the form to add a new user."""
    
    return render_template("addUser.html")

@app.route('/users/new', methods=["POST"])
def handle_new_user():
    """Handles submission of a new user. Then redirects to list of all users."""
   
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Shows user details for user with id of user_id. Includes links to edit user information or delete user."""

    user = User.query.get_or_404(user_id)
    return render_template("userDetails.html", user = user)

@app.route('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    """Shows edit page for user with id of user_id. Includes link to cancel edits, which returns to user's detail page. Includes save button to update user."""
    
    user = User.query.get_or_404(user_id)
    return render_template("editUser.html", user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user(user_id):
    """Processes submitted edits for user with id of user_id and redirects to list of all users."""
    
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """Processes deletion of user with id user_id. Redirects to list of all users."""

    # Check if user exists with this line
    user = User.query.get_or_404(user_id)


    # Assuming user exists, delete them
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show form to add a post for the user specified."""

    user = User.query.get_or_404(user_id)

    return render_template('createPost.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post_submission(user_id):
    """Handle the addition of a new post for specified user and redirect to user's details page."""

    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    created_by = user.id

    post = Post(title=title, content=content, created_by=created_by)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the specified post, with buttons to edit and delete it."""

    post = Post.query.get_or_404(post_id)
    return render_template('postDetails.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit the specified post, with buttons to cancel and save."""

    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_submission(post_id):
    """Handle submitted edits to specified post and redirect to that post's details page."""

    post = Post.query.get_or_404(post_id)
    user = post.creator.id

    post.title = request.form['title']
    post.content = request.form['content']
    post.created_by = user

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def handle_post_deletion(post_id):
    """Handle deletion of specified post and redirect to creator's details page."""

    # Check if post exists with this line
    post = Post.query.get_or_404(post_id)

    # Assuming the post exists, grab the creator's id and delete the post
    user_id = post.creator.id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')