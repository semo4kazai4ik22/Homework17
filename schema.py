from marshmallow import Schema, fields


class Movie(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    director_id = fields.Integer()


class Director(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class Genre(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()