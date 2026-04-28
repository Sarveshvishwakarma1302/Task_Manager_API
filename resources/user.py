from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt

from models.user import User
from models.task import Task
from models.task_status import TaskStatus

blp = Blueprint("users", __name__)

#ADMIN CHECK
def is_admin():
    return get_jwt().get("role") == "admin"


#Fetch Users
@blp.route("/users")
class UserList(MethodView):

    @jwt_required()
    def get(self):

        if not is_admin():
            return {"message": "Admin only"}, 403

        users = User.query.all()

        return {
            "users": [
                {
                    "id": u.id,
                    "username": u.username,
                    "role": u.role
                }
                for u in users
            ]
        }


# User Own Dashboard
@blp.route("/users/<int:user_id>/tasks")
class UserDashboard(MethodView):

    @jwt_required()
    def get(self, user_id):

        if not is_admin():
            return {"message": "Admin only"}, 403

        assignments = TaskStatus.query.filter_by(user_id=user_id).all()

        result = []

        for a in assignments:
            task = Task.query.get(a.task_id)

            result.append({
                "task_id": task.id,
                "title": task.title,
                "status": a.status
            })

        return {
            "user_id": user_id,
            "tasks": result
        }


# Admin dashboard
@blp.route("/dashboard")
class AdminDashboard(MethodView):

    @jwt_required()
    def get(self):

        if not is_admin():
            return {"message": "Admin only"}, 403

        assignments = TaskStatus.query.all()

        result = []

        for a in assignments:
            user = User.query.get(a.user_id)
            task = Task.query.get(a.task_id)

            result.append({
                "user_id": user.id,
                "username": user.username,
                "task_id": task.id,
                "title": task.title,
                "status": a.status
            })

        return {"dashboard": result}