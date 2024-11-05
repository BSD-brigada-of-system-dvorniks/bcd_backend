from mongoengine import Document, fields


class Object(Document):

	TYPE_OPTIONS = ('Green', 'Yellow', 'Red')

	name = fields.StringField(max_length = 128, required = True)
	type = fields.StringField(choices = TYPE_OPTIONS)
	level = fields.IntField(min_value = 1, max_value = 5)
	text = fields.StringField()

	published = fields.BooleanField(required = True, default = False)

	def __str__(self):
		return f"{self.name}"
