from tests.base import BaseTestCase


class TestUsers(BaseTestCase):

    def get_admin_token(self):
        self.client.post("/register", json={
            "username": "admin",
            "password": "123456",
            "role": "admin"
        })

        res = self.client.post("/login", json={
            "username": "admin",
            "password": "123456"
        })

        return res.get_json()["access_token"]

    # Admin can access users
    def test_get_users_admin(self):
        token = self.get_admin_token()

        res = self.client.get(
            "/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)

    # Non-admin cannot access
    def test_get_users_non_admin(self):
        self.client.post("/register", json={
            "username": "user1",
            "password": "123456",
            "role": "user"
        })

        res = self.client.post("/login", json={
            "username": "user1",
            "password": "123456"
        })

        token = res.get_json()["access_token"]

        res = self.client.get(
            "/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 403)

    # No token → Unauthorized
    def test_get_users_no_token(self):
        res = self.client.get("/users")
        self.assertEqual(res.status_code, 401)

    # Invalid token
    def test_invalid_token(self):
        res = self.client.get(
            "/users",
            headers={"Authorization": "Bearer wrongtoken"}
        )
        self.assertEqual(res.status_code, 422)

    # Users list structure
    def test_users_response_structure(self):
        token = self.get_admin_token()

        res = self.client.get(
            "/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        data = res.get_json()

        self.assertIn("users", data)
        self.assertIsInstance(data["users"], list)