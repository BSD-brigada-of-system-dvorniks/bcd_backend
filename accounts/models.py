import secrets

from mongoengine import Document, fields
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document):
    username = fields.StringField(required = True, unique = True)
    email    = fields.EmailField(required  = True, unique = True)
    password = fields.StringField(required = True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Token(Document):
    key  = fields.StringField(required = True, unique = True)
    user = fields.ReferenceField(User, required = True)

    @staticmethod
    def generate_key():
        return secrets.token_hex(16)

    @classmethod
    def create_token(cls, user):
        existing_token = cls.objects(user = user).first()
        if existing_token:
            return existing_token

        token = cls(key = cls.generate_key(), user = user)
        token.save()
        return token
