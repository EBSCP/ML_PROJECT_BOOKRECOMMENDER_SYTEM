import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Dataset yolunu projeye göre ayarla
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'books', 'books_dataset.csv')

# Dataseti yükle
df = pd.read_csv(DATA_PATH)
df['description'] = df['description'].fillna("")  # Eksik açıklamaları boş bırakma

# TF-IDF hesaplama
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'])

# Kitap başlıklarına göre index oluştur
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations_with_similarity(title, author, top_n=10):
    # Kitap adı ve yazarıyla eşleşen kitapları bulalım
    matches = df[df['title'].str.contains(title, case=False, na=False) & df['authors'].str.contains(author, case=False, na=False)]
    if matches.empty:
        return pd.DataFrame()  # Eğer eşleşen kitap yoksa boş dönebiliriz

    # Kısmi eşleşme ile bulunan kitapların index'lerini alalım
    idx = matches.index.tolist()

    # Benzerlik hesaplaması
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    sim_scores = []
    for i in idx:
        sim_scores.append(list(enumerate(cosine_sim[i])))

    # Tüm kitaplar için benzerlik skoru hesaplayıp, sıralama yapalım
    sim_scores = [item for sublist in sim_scores for item in sublist]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    book_indices = [i[0] for i in sim_scores]
    similarities = [round(score * 100, 2) for _, score in sim_scores]

    # Benzerlik oranlarını ve görselleri dahil ediyoruz
    # Benzerlik oranlarını ve görselleri dahil ediyoruz
    recommendations = df[['title', 'authors', 'average_rating', 'thumbnail', 'description']].iloc[book_indices].copy()
    recommendations['similarity_percentage'] = similarities  # Burada 'similarity_percentage' olarak ekliyoruz

    return recommendations


def get_books_and_authors_by_title(title):
    # Kitap adıyla eşleşen kitapları bul
    matches = df[df['title'].str.contains(title, case=False, na=False)]
    
    # Eşleşen kitapların başlık ve yazarlarını al
    books = [{'title': row['title'], 'author': row['authors']} for _, row in matches.iterrows()]
    
    return books

