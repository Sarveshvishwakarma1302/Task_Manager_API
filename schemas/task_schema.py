from marshmallow import Schema, fields, validate, validates_schema, ValidationError

# CONSTANTS
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUS = ["pending", "in-progress", "completed"]


# CREATE TASK (ONLY TASK DATA)

class TaskCreateSchema(Schema):

    title = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100)
    )

    description = fields.Str(
        required=False,
        validate=validate.Length(max=250)
    )

    # priority validation
    priority = fields.Str(
        load_default="low",
        validate=validate.OneOf(VALID_PRIORITIES)
    )

# Assignment API
class TaskAssignSchema(Schema):

    task_id = fields.Int(required=True)

    usernames = fields.List(
        fields.Str(),
        required=True,
        validate=validate.Length(min=1)
    )

# Update API
class TaskStatusSchema(Schema):

    status = fields.Str(
        required=True,
        validate=validate.OneOf(VALID_STATUS)
    )

class TaskUpdateSchema(Schema):

    title = fields.Str(required=False)
    description = fields.Str(required=False)

    # ADD THIS (ADMIN CAN UPDATE PRIORITY)
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(["low", "medium", "high"])
    )

    status = fields.Str(
        required=False,
        validate=validate.OneOf(["pending", "in-progress", "completed"])
    )