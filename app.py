"""Blogly application."""
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def redirect_to_users():
    """Redirect to list of users."""

    return redirect("/users")


@app.route("/users")
def list_users():
    """List users on homepage."""

    users = User.query.all()
    return render_template("user_listing.html", users=users)


@app.route("/users/new")
def new_user():
    """Show add form."""

    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def post_new_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] if request.form['image_url'] else None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)

    try:
        posts = Post.query.filter_by(author_id=user.id).all()
    except NameError:
        return render_template("user_details.html", user=user)

    return render_template("user_details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def post_edit_user(user_id):
    """Submit edited info on a single user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    try:
        tags = Tag.query.all()
    except NameError:
        return render_template('new_post_form.html', user=user)

    return render_template("new_post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_new_post_form(user_id):
    """Aadd post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')
    post = Post(title=title, content=content, author_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route("/posts/<int:post_id>")
def show_posts(post_id):
    """Show post from post id."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.author_id)

    return render_template("post_details.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit")
def show_edit_posts(post_id):
    """Show form to edit a post, and to cancel."""

    post = Post.query.get_or_404(post_id)

    return render_template("edit_post_form.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def submit_edit_posts(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    post.created_at = datetime.now()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users')


@app.route("/tags")
def list_tags():
    """List tags."""

    try:
        tags = Tag.query.all()
    except NameError:
        return render_template('list_tags.html')

    return render_template('list_tags.html', tags=tags)


@app.route("/tags/<int:tag_id>")
def show_posts(tag_id):
    """Show detail about a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("show_tag.html", tag=tag)


@app.route("/tags/new")
def add_new_tag():
    """Shows a form to add a new tag."""

    return render_template("add_tag.html")


@app.route("/tags/new", methods=['POST'])
def submit_new_tag():
    """Process add form, adds tag, and redirect to tag list."""

    name = request.form['name']
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tags(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=['POST'])
def submit_edit_tags(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=['POST'])
def delete_tag(tag_id):
    """Delete the tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect(f'/tags')


if __name__ == '__main__':
    app.run()
