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




def advanced_search_books(df, title=None, author=None, categories=None, labels=None, min_rating=None, max_rating=None, top_n=20):
    """
    Gelişmiş arama fonksiyonu.
    df: kitapların olduğu DataFrame
    title, author, categories, labels: string, None ise filtre yok.
    min_rating: float veya None
    top_n: kaç sonuç döndürülecek
    
    labels: virgülle ayrılmış etiketler string şeklinde gelebilir, ona göre filtre yaparız.
    """

    filtered = df.copy()

    if title:
        filtered = filtered[filtered['title'].str.contains(title, case=False, na=False)]

    if author:
        filtered = filtered[filtered['authors'].str.contains(author, case=False, na=False)]

    if categories:
        # Kategori alanı içinde girilen string veya stringler var mı diye kontrol et
        for cat in categories.split(','):
            cat = cat.strip()
            filtered = filtered[filtered['categories'].str.contains(cat, case=False, na=False)]

    if labels:
        # Datasette label yok ama description içinde etiket gibi kelimeler arayabiliriz.
        # labels stringi virgülle ayrılmış olabilir
        for label in labels.split(','):
            label = label.strip()
            filtered = filtered[filtered['description'].str.contains(label, case=False, na=False)]

    if min_rating:
        try:
            rating_float = float(min_rating)
            filtered = filtered[filtered['average_rating'] >= rating_float]
        except ValueError:
            pass
    # Sonuçları rating'e göre sıralayıp ilk top_n kitabı döndür
    filtered = filtered.sort_values(by='average_rating', ascending=False)

    if max_rating:
        try:
            rating_float = float(max_rating)
            filtered = filtered[filtered['average_rating'] <= rating_float]
        except ValueError:
            pass
    # Sonuçları rating'e göre sıralayıp ilk top_n kitabı döndür
    filtered = filtered.sort_values(by='average_rating', ascending=False)

    return filtered.head(top_n)


def get_multi_book_recommendations(titles, df=df, tfidf=tfidf, tfidf_matrix=tfidf_matrix):
    descriptions = []
    indices_to_exclude = []

    for title in titles:
        idx = indices.get(title)
        if idx is not None:
            desc = df.loc[idx, 'description']
            descriptions.append(str(desc))
            indices_to_exclude.append(idx)
        else:
            print(f"Kitap bulunamadı: {title}")

    if not descriptions:
        return pd.DataFrame()

    combined_description = " ".join(descriptions)
    query_vec = tfidf.transform([combined_description])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    for idx in indices_to_exclude:
        cosine_similarities[idx] = -1

    top_indices = cosine_similarities.argsort()[::-1][:5]
    similarities = [round(cosine_similarities[i] * 100, 2) for i in top_indices]

    results = df[['title', 'authors','categories' ,'average_rating', 'thumbnail', 'description']].iloc[top_indices].copy()
    results['similarity_percentage'] = similarities

    return results
