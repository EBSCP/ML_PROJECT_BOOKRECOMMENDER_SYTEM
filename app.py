from flask import Flask, render_template, request, jsonify
import os
from model.recommender import get_recommendations_with_similarity, get_books_and_authors_by_title, advanced_search_books
from model.recommender import get_multi_book_recommendations  # bu fonksiyon da import edilmeli
import pandas as pd

app = Flask(__name__)


# Dataset yolunu projeye göre ayarla
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'books', 'books_dataset.csv')

# Dataseti yükle
df = pd.read_csv(DATA_PATH)
df['description'] = df['description'].fillna("")  # Eksik açıklamaları boş bırakma

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    title = None
    author = None

    if request.method == 'POST':
        book_info = request.form['book_info']
        title, author = book_info.split(',')
        
        recommendations = get_recommendations_with_similarity(title, author)

    return render_template('index.html', recommendations=recommendations, title=title, author=author)


@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    recommendations = None

    if request.method == 'POST':
        title = request.form.get('title', '').strip() or None
        author = request.form.get('author', '').strip() or None
        categories = request.form.get('categories', '').strip() or None
        labels = request.form.get('label', '').strip() or None
        min_rating = request.form.get('min_rating', '').strip() or None
        max_rating = request.form.get('max_rating', '').strip() or None
        
        recommendations = advanced_search_books(df, title, author, categories, labels, min_rating, max_rating, top_n=20)

    return render_template('advanced_search.html', recommendations=recommendations)


@app.route('/multi_book_recommend', methods=['POST'])
def multi_book_recommend():
    recommendations = None
    titles_raw = request.form.get('multi_titles', '')
    titles = [t.strip() for t in titles_raw.split(',') if t.strip()]

    if titles:
        recommendations = get_multi_book_recommendations(titles)

    return render_template('advanced_search.html', recommendations=recommendations)


@app.route('/get_books_and_authors', methods=['GET'])
def get_books_and_authors():
    title = request.args.get('title')
    books = get_books_and_authors_by_title(title)
    return jsonify({'books': books})

if __name__ == '__main__':
    app.run(debug=True)