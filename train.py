import pandas as pd
from model.Content_model import build_content_model
from model.collaborative_model import train_svd_model
from api.hybrid import hybrid_recommendations
import pickle

# Verileri yükle
books = pd.read_csv("./data_sets/Books.csv", sep=';')
ratings = pd.read_csv("./data_sets/Ratings_book.csv", sep=';')

# Kolon isimlerini düzenle
books.columns = ['isbn', 'title', 'author', 'year', 'publisher']
ratings.columns = ['user_id', 'isbn', 'rating']

# Eksik verileri doldur ve 'genres' sütunu oluştur
books['genres'] = books[['author', 'publisher']].fillna('').agg(' '.join, axis=1)

# Örnekleme
books_sample = books.head(10000)

# Modelleri oluştur
cosine_sim, indices = build_content_model(books_sample)
svd_model = train_svd_model(ratings)

# Öneri örneği
print(hybrid_recommendations(10000, "The Fellowship of the Ring (The Lord of the Rings, Part 1)", books_sample, cosine_sim, indices, svd_model, top_n=10))

# Modelleri kaydet
with open("cosine_sim.pkl", "wb") as f:
    pickle.dump(cosine_sim, f)
with open("indices.pkl", "wb") as f:
    pickle.dump(indices, f)
with open("svd_model.pkl", "wb") as f:
    pickle.dump(svd_model, f)