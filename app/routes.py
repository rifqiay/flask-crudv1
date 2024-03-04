import os
from . import create_app
from .models import Book, to_json
from flask import jsonify, abort, request
from . import db

app = create_app(os.getenv('MACHINE'))

@app.route("/", methods=["GET"])
def index_route():
    return {
        "message": 'server running properly',
        "status": 200
    }

@app.route("/book", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([to_json(book) for book in books])

@app.route("/book/<int:isbn>", methods=["GET"])
def get_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    return to_json(book)

@app.route("/book/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"result": True})

@app.route("/book", methods=["POST"])
def create_book():
    if not request.json:
        abort(404)

    book = Book(
        isbn = request.json.get('isbn'),
        title = request.json.get('title'),
        author = request.json.get('author'),
        price = request.json.get('price')
    )

    db.session.add(book)
    db.session.commit()
    return jsonify(to_json(book)), 201

@app.route("/book/<int:isbn>", methods=["PUT"])
def update_book(isbn):
    if not request.json:
        abort(404)
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    book.title = request.json.get('title', book.title)
    book.author = request.json.get('author', book.author)
    book.price = request.json.get('price', book.price)

    db.session.commit()
    return jsonify(to_json(book))