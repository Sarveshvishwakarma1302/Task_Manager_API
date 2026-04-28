from tests.base import BaseTestCase


class TestDashboard(BaseTestCase):

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

    def get_user_token(self):
        self.client.post("/register", json={
            "username": "user1",
            "password": "123456",
            "role": "user"
        })

        res = self.client.post("/login", json={
            "username": "user1",
            "password": "123456"
        })

        return res.get_json()["access_token"]

    #  Admin dashboard test
    def test_admin_dashboard(self):
        token = self.get_admin_token()

        # create additional user
        self.client.post("/register", json={
            "username": "user2",
            "password": "123456",
            "role": "user"
        })

        res = self.client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["role"], "admin")

        # important fields
        self.assertIn("total_users", data)
        self.assertIn("total_tasks", data)
        self.assertIn("total_completed_tasks", data)
        self.assertIn("total_pending_tasks", data)
        self.assertIn("user_stats", data)

        self.assertIsInstance(data["user_stats"], list)

    #  User dashboard test
    def test_user_dashboard(self):
        token = self.get_user_token()

        res = self.client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["role"], "user")

        self.assertIn("tasks", data)
        self.assertIsInstance(data["tasks"], list)