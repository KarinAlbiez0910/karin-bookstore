from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    name = db.Column(db.String(200), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(200), nullable=False)

#db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<user>')
def display_profile(user):
    return render_template('profile.html', user=user, is_active=False)

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/add-book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        new_book = Book(
            name=request.form.get("name"),
            author=request.form.get("author")
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('addbook.html')

@app.route('/edit_book/<book_name>', methods=['POST', 'GET'])
def edit_book(book_name):
    book = Book.query.filter_by(name=book_name).first()
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_author = request.form.get('author')
        print(new_name, new_author)
        book.name = new_name
        book.author = new_author
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('editbook.html', book=book)

@app.route('/delete_book/<book_name>')
def delete_book(book_name):
    book = Book.query.filter_by(name=book_name).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books'))

if __name__ == "__main__":
    app.run()