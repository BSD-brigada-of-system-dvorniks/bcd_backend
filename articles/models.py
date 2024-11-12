from mongoengine import Document, EmbeddedDocument, fields

from accounts.models import User


class Article(EmbeddedDocument):
    name = fields.StringField(max_length = 128, required = True)
    text = fields.StringField(max_length = 256_000)
    published = fields.BooleanField(required = True, default = False)
    author = fields.ReferenceField(User, null = True)

    def __str__(self):
        return f"DOC - {self.name}"


class Object(Document):

    TYPE_OPTIONS = ('Green', 'Yellow', 'Red')

    type = fields.StringField(choices = TYPE_OPTIONS)
    level = fields.IntField(min_value = 1, max_value = 5)
    article = fields.EmbeddedDocumentField(Article)

    def __str__(self):
        return f"BCD - {self.article.name}"
