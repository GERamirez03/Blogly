from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User."""

        with app.app_context():
            User.query.delete()

            user = User(first_name="Test", last_name="User", image_url="https://cdn-icons-png.flaticon.com/512/25/25634.png")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transactions."""

        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            print(self.user_id)
            response = client.get(f"/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h2>Test User</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "Demo", "last_name": "User", "image_url": "https://cdn-icons-png.flaticon.com/512/5229/5229448.png"}
            response = client.post("/users/new", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Demo User', html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {"first_name": "Beta", "last_name": "Tester", "image_url": "https://qa.world/wp-content/uploads/2020/11/beta-testing.png"}
            response = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Beta Tester', html)