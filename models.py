"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


""" Users table """


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(20),
                           nullable=False)
    last_name = db.Column(db.String(20),
                          nullable=False)
    image_url = db.Column(db.String(), nullable=True,
                          default='https://images.unsplash.com/photo-1591102972305-213abaa76d6f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=676&q=80')

    posts = db.relationship('Post', backref='user', cascade='all, delete')

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def fullname(self):
        """ Get users full name """
        return self.first_name + ' ' + self.last_name


""" Posts table """


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(30),
                      nullable=False)
    content = db.Column(db.String(),
                        nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now())
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """Show info about post."""

        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at}>"

    def format_date(self):
        """ Show nicely formatted date """

        return self.created_at.strftime('%a %b %-d %Y, %-H:%M')


""" Tags table """


class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(20), unique=True,
                     nullable=False)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all,delete",
        backref="tags",
    )

    def __repr__(self):
        """Show info about post."""

        t = self
        return f"<Tag {t.id} {t.title} {t.content} {t.created_at}>"


""" PostTags table """


class PostTag(db.Model):
    """PostTag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True,
                        nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True,
                       nullable=False)

    def __repr__(self):
        """Show info about posts and tags."""

        pt = self
        return f"<PostTag {pt.id} {pt.tag_id}>"
