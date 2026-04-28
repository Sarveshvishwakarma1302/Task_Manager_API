from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import db
from models.task import Task
from models.task_status import TaskStatus
from models.task_assignment import TaskAssignment
from models.user import User

from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema

blp = Blueprint("tasks", __name__)


def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == "admin"

#Task Routes
@blp.route("/tasks")
class TaskList(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        status_filter = request.args.get("status")

        results = []


        if is_admin():

            tasks = Task.query.all()

            for task in tasks:

                # Admin uses TASK.status (global)
                status = task.status

                if status_filter and status != status_filter:
                    continue

                results.append({
                    "id": task.id,
                    "title": task.title,
                    "priority": task.priority,
                    "status": status,
                    "description":task.description
                    
                })

        # Filteration
        else:

            assignments = TaskAssignment.query.filter_by(
                user_id=user_id
            ).all()

            for a in assignments:

                task = db.session.get(Task, a.task_id)
                if not task:
                    continue

                # User uses TaskStatus (personal progress)
                task_status = TaskStatus.query.filter_by(
                    task_id=task.id,
                    user_id=user_id
                ).first()

                # If no record → default pending
                status = task_status.status if task_status else "pending"

                if status_filter and status != status_filter:
                    continue

                results.append({
                    "id": task.id,
                    "title": task.title,
                    "priority": task.priority,
                    "status": status,
                    "assigned_at": a.assigned_at,
                    "deadline": a.deadline,
                    "is_overdue": datetime.utcnow() > a.deadline if a.deadline else False
                    
                })

        # Pagination
        start = (page - 1) * limit
        end = start + limit

        return {
            "tasks": results[start:end],
            "page": page,
            "limit": limit,
            "total": len(results)
        }

    # Create Task
    @jwt_required()
    @blp.arguments(TaskCreateSchema)
    def post(self, data):

        if not is_admin():
            return {"message": "Admin only"}, 403

        task = Task(
            title=data["title"],
            description=data.get("description"),
            priority=data.get("priority", "low"),
            user_id=get_jwt_identity(),
            status="pending"
        )

        db.session.add(task)
        db.session.commit()

        return {
            "message": "Task created successfully",
            "task_id": task.id
        }


@blp.route("/assign-task")
class AssignTaskAPI(MethodView):

    @jwt_required()
    def post(self):

        if not is_admin():
            return {"message": "Admin only"}, 403

        data = request.get_json()

        task_id = data.get("task_id")
        usernames = data.get("usernames", [])

        task = db.session.get(Task, task_id)
        if not task:
            return {"message": "Task not found"}, 404

        users = User.query.filter(User.username.in_(usernames)).all()

        found_usernames = {u.username for u in users}
        requested_usernames = set(usernames)

        missing_users = requested_usernames - found_usernames

        if missing_users:
            return {
                "message": "Some users not found",
                "invalid_users": list(missing_users)
            }, 400

        # Time Duration
        for user in users:

            assigned_time = datetime.utcnow()

            if task.priority == "high":
                duration = timedelta(hours=24)
            elif task.priority == "medium":
                duration = timedelta(days=7)
            else:
                duration = timedelta(days=14)

            deadline = assigned_time + duration

            db.session.add(TaskAssignment(
                task_id=task.id,
                user_id=user.id,
                assigned_at=assigned_time,
                deadline=deadline
            ))

        db.session.commit()

        return {
            "message": "Task assigned successfully",
            "assigned_users": list(found_usernames)
        }


# Update Task
@blp.route("/tasks/<int:task_id>")
class TaskResource(MethodView):


    @jwt_required()
    @blp.arguments(TaskUpdateSchema)
    def put(self, data, task_id):

        task = db.session.get(Task, task_id)
        if not task:
            return {"message": "Task not found"}, 404

        user_id = get_jwt_identity()


        if is_admin():

            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.status = data.get("status", task.status)
            task.priority = data.get("priority", task.priority)

            db.session.commit()

            return {"message": "Task updated (admin)"}


        if "title" in data or "description" in data:
            return {"message": "Not allowed"}, 403

        status = data.get("status")
        if not status:
            return {"message": "Status required"}, 400

        ts = TaskStatus.query.filter_by(
            task_id=task_id,
            user_id=user_id
        ).first()

        if not ts:
            ts = TaskStatus(task_id=task_id, user_id=user_id)

        ts.status = status

        db.session.add(ts)
        db.session.commit()

        return {"message": "Status updated"}

    # Delete Task
    @jwt_required()
    def delete(self, task_id):

        if not is_admin():
            return {"message": "Admin only"}, 403

        task = db.session.get(Task, task_id)
        if not task:
            return {"message": "Task not found"}, 404

        TaskAssignment.query.filter_by(task_id=task_id).delete()
        TaskStatus.query.filter_by(task_id=task_id).delete()

        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted"}