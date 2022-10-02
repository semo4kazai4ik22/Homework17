# app.py

from flask import Flask, request
from flask_restx import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)
api = Api(app)

movies_ns = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")

movies_schema = schema.Movie(many=True)
movie_schema = schema.Movie()

directors_schema = schema.Director(many=True)
director_schema = schema.Director()

genres_schema = schema.Genre(many=True)
genre_schema = schema.Genre()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id: object = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movies_ns.route("/")
class MovieView(Resource):
    def get(self):
        movies = db.session.query(Movie)

        args = request.args

        director_id = args.get('director_id')

        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)

        genre_id = args.get('genre_id')

        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)

        movies_query = movies.all()

        return movies_schema.dump(movies_query), 200


@movies_ns.route("/<int:mid>")
class MovieViewId(Resource):
    def get(self, mid):
        movie = db.session.query(Movie).get(mid)

        if movie is None:
            return {}, 404

        return movie_schema.dump(movie), 200

    def put(self, mid):
        updated_row = db.session.query(Movie).filter(Movie.id == mid).update(request.json)

        if updated_row != 1:
            return None, 400

        db.session.commit()

        return None, 204

    def delete(self, mid):
        deleted_row = db.session.query(Movie).filter(Movie.id == mid).delete()

        if deleted_row != 1:
            return None, 400

        db.session.commit()

        return None, 200

    def post(self):
        new_row = Movie(**request.json)
        with db.session.begin():
            db.session.add(new_row)
        return "", 201


@directors_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director).all()

        return directors_schema.dump(directors), 200


@directors_ns.route("/<int:did>")
class DirectorViewId(Resource):
    def get(self, did):
        director = db.session.query(Director).get(did)

        if director is None:
            return {}, 404

        return director_schema.dump(director), 200


@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre).all()

        return genres_schema.dump(genres), 200


@genres_ns.route("/<int:gid>")
class GenreViewId(Resource):
    def get(self, gid):
        genre = db.session.query(Genre).get(gid)

        if genre is None:
            return {}, 404

        return genre_schema.dump(genre), 200


if __name__ == '__main__':
    app.run(debug=True)
