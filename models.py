"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(25),
                           nullable=False)
    last_name = db.Column(db.String(25),
                          nullable=False)
    image_url = db.Column(db.String(200),
                          default="https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-7509.jpg?w=996")
    
class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(
            db.Integer,
            primary_key=True,
            autoincrement=True)
    
    title = db.Column(
            db.String(50),
            nullable=False)
    
    content = db.Column(
            db.Text,
            nullable=False)
    
    created_at = db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.now)
    
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    creator = db.relationship('User', backref='posts')

class Tag(db.Model):
    """Tag for a post."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    name = db.Column(
        db.Text,
        nullable=False,
        unique=True)
    
    posts = db.relationship('Post',
                            secondary='posts_tags',
                            backref='tags') # does using the POSTS_tags table mean that this is supposed to start in the POSTS class?
    
    postTags = db.relationship('PostTag', backref='tag', passive_deletes=True)
    
# I need help with implementing a cascading delete so that when a tag gets deleted, the rows of PostTag with that tag also get deleted.

class PostTag(db.Model):
    """Relation of posts to the tags that they have."""
    
    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True)
    
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"), on_delete='CASCADE',
        primary_key=True)
    
    tags = db.relationship('Tag', cascade="all,delete", backref="post_tags", passive_deletes=True)

# I need help with on cascade, deleting the relevant relationships...
# eg Delete a tag, delete the PostTags that reference it
# eg Delete a post, delete the PostTags that reference it