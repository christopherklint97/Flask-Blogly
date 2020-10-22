import os
from unittest import TestCase
from app import app
from models import db, User, Post


# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        user = User(first_name="John", last_name="Appleseed")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Appleseed', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Appleseed</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "Jessica", "last_name": "Jones",
                    "image_url": 'https://images.unsplash.com/photo-1554151228-14d9def656e4?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=333&q=80'}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jessica Jones", html)


class PostViewsTestCase(TestCase):
    """Tests for views for Post."""

    def setUp(self):
        """Add sample post and user."""

        user = User(first_name="Bob", last_name="Dillan")
        post = Post(title="This is a test",
                    content="This is also a test", author_id=1)

        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'This is a test', html)

    def test_add_post(self):
        with app.test_client() as client:
            data = {"title": "Status update", "content": "Just got out of the shower, yay me!",
                    "author_id": 1}
            resp = client.post("/users/1/posts/new",
                               data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'Status update', html)
