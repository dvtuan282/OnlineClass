from pprint import pprint
from datetime import datetime
from marshmallow import Schema, fields

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.utcnow()

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

class Blog:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class BlogSchema(Schema):
    title = fields.Str()
    author = fields.Nested(UserSchema)

# Creating a User instance
user = User(name="Monty", email="monty@python.org")

# Creating a Blog instance with the User instance as the author
blog = Blog(title="Something Completely Different", author=user)

# Serializing the Blog instance using BlogSchema
result = BlogSchema().dump(blog)

# Pretty-printing the serialized result
pprint(result)
