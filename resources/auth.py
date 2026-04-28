from flask_smorest import Blueprint
from flask.views import MethodView
from models import db
from models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# SCHEMA IMPORT
from schemas.user_schema import UserRegisterSchema, UserLoginSchema

blp = Blueprint("auth", __name__)

# REGISTER
@blp.route("/register")
class Register(MethodView):

    @blp.arguments(UserRegisterSchema)
    def post(self, data):

        user = User(
            username=data["username"].strip(),
            password=generate_password_hash(data["password"]),
            role=data["role"]
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}
    
# LOGIN
@blp.route("/login")
class Login(MethodView):

    @blp.arguments(UserLoginSchema)
    def post(self, data):

        user = User.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.role}
            )
            # return {"token": token}
            return {"access_token": access_token }

        return {"message": "Invalid credentials"}, 401