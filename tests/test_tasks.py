from tests.base import BaseTestCase


class TestTasks(BaseTestCase):

# Tokens For Admin
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

# Create user
    def create_user(self, username):
        self.client.post("/register", json={
            "username": username,
            "password": "123456",
            "role": "user"
        })

# Create Task
    def test_create_task(self):
        token = self.get_admin_token()

        res = self.client.post(
            "/tasks",
            json={
                "title": "Task1",
                "priority": "high"
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)


    def test_assign_task(self):
        token = self.get_admin_token()

        self.create_user("user1")
        self.create_user("user2")

        # create task first
        task_res = self.client.post(
            "/tasks",
            json={"title": "Task2"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # get created task id
        tasks_res = self.client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = tasks_res.get_json()["tasks"][0]["id"]

        # assign task
        res = self.client.post(
            "/assign-task",
            json={
                "task_id": task_id,
                "usernames": ["user1", "user2"]
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)

# Assign Task
    def test_assign_invalid_user(self):
        token = self.get_admin_token()

        # create task
        self.client.post(
            "/tasks",
            json={"title": "Task3"},
            headers={"Authorization": f"Bearer {token}"}
        )

        tasks_res = self.client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = tasks_res.get_json()["tasks"][0]["id"]

        # assign invalid user
        res = self.client.post(
            "/assign-task",
            json={
                "task_id": task_id,
                "usernames": ["fakeUser"]
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 400)

# Get Task
    def test_get_tasks(self):
        token = self.get_admin_token()

        res = self.client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)

# Update Task
    def test_update_task_status(self):
        token = self.get_admin_token()

        self.create_user("user1")

        # create task
        self.client.post(
            "/tasks",
            json={"title": "Task4"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # get task id
        tasks_res = self.client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = tasks_res.get_json()["tasks"][0]["id"]

        # assign task first
        self.client.post(
            "/assign-task",
            json={
                "task_id": task_id,
                "usernames": ["user1"]
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        # update status
        res = self.client.put(
            f"/tasks/{task_id}",
            json={"status": "completed"},
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)

# Delete Task
    def test_delete_task(self):
        token = self.get_admin_token()

        # create task
        self.client.post(
            "/tasks",
            json={"title": "Task5"},
            headers={"Authorization": f"Bearer {token}"}
        )

        tasks_res = self.client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = tasks_res.get_json()["tasks"][0]["id"]

        # delete
        res = self.client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(res.status_code, 200)