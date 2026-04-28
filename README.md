# Task Manager API (Flask REST API)

A role-based **Task Management REST API** built using Flask.  
It supports authentication, task assignment, role-based access control, dashboards, and full CRUD operations with proper validation and testing.

# Features

# Authentication & Authorization
- User Registration & Login
- JWT-based authentication
- Role-based access control (Admin / User)

# Task Management
- Create tasks (Admin only)
- Assign tasks to multiple users
- Update task status
- Delete tasks (Admin only)
- Priority-based task handling (low, medium, high)

# User Features
- View assigned tasks
- Update own task status
- Personal task tracking

# Dashboards
- Admin dashboard: all users + all tasks overview
- User dashboard: personal assigned tasks

# Advanced Features
- Task deadlines based on priority
- Status tracking (pending, in-progress, completed)
- Pagination & filtering support
- Input validation using Marshmallow

# Tech Stack

- Python 
- Flask
- Flask-Smorest (REST API framework)
- Flask-JWT-Extended (Authentication)
- Flask-SQLAlchemy (ORM)
- Marshmallow (Validation & Serialization)
- SQLite (Database)
- Unittest (Testing)

# Project Structure

Task_Manager/
│
├── models/ # Database models
├── resources/ # API routes (controllers)
├── schemas/ # Validation schemas
├── tests/ # Unit tests
├── app.py # Application entry point
├── db.py # Database initialization
└── .gitignore

API Endpoints
Auth
POST /register → Register user
POST /login → Login user
Tasks
GET /tasks → Get all tasks
POST /tasks → Create task (Admin)
PUT /tasks/<id> → Update task (Admin Fully/user Partially)
DELETE /tasks/<id> → Delete task (Admin)
POST /assign-task → Assign task to users (Admin) (Many To Many)

Security Features
JWT Authentication
Role-based authorization
Environment variable protection (.env)
Input validation using Marshmallow
Secure password hashing

Admin
Create tasks
Assign tasks (Many To Many)
View all users
Access dashboard
User
View assigned tasks 
Update task status
