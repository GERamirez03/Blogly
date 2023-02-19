"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
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

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')