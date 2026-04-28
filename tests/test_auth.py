from tests.base import BaseTestCase

class TestAuth(BaseTestCase):

    #  Register success
    def test_register_success(self):
        res = self.client.post("/register", json={
            "username": "testuser",
            "password": "123456",
            "role": "user"
        })
        self.assertEqual(res.status_code, 200)

    #  Duplicate username
    def test_register_duplicate(self):
        self.client.post("/register", json={
            "username": "testuser",
            "password": "123456",
            "role": "user"
        })
        res = self.client.post("/register", json={
            "username": "testuser",
            "password": "123456",
            "role": "user"
        })
        self.assertNotEqual(res.status_code, 200)

    #  Password too short
    def test_register_short_password(self):
        res = self.client.post("/register", json={
            "username": "user2",
            "password": "123",
            "role": "user"
        })
        self.assertEqual(res.status_code, 422)

    #  Missing field
    def test_register_missing_field(self):
        res = self.client.post("/register", json={
            "username": "user3"
        })
        self.assertEqual(res.status_code, 422)

    #  Login success
    def test_login_success(self):
        self.client.post("/register", json={
            "username": "loginuser",
            "password": "123456",
            "role": "user"
        })

        res = self.client.post("/login", json={
            "username": "loginuser",
            "password": "123456"
        })
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertIn("access_token", data)  