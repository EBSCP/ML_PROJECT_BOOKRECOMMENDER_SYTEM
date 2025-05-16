from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# CORS ayarları (Angular için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dosya yolları
base_dir = os.path.dirname(os.path.abspath(__file__))
books_path = os.path.join(base_dir, "..", "data_sets", "Books.csv")
ratings_path = os.path.join(base_dir, "..", "data_sets", "Ratings_book.csv")

# CSV'leri oku
books_df = pd.read_csv(books_path, sep=';', encoding='latin1')
ratings_df = pd.read_csv(ratings_path, sep=';', encoding='latin1')

# Sütun isimlerini temizle
books_df.columns = books_df.columns.str.strip()
ratings_df.columns = ratings_df.columns.str.strip()

# Eksik kayıtları temizle
books_df = books_df.dropna(subset=["ISBN", "Title"])
ratings_df = ratings_df[ratings_df["Rating"] > 0]

# Ortalama puanları ISBN'e göre hesapla
avg_ratings = ratings_df.groupby("ISBN")["Rating"].mean().reset_index()
avg_ratings.rename(columns={"Rating": "est_rating"}, inplace=True)

# Kitaplarla puanları birleştir
books_df = pd.merge(books_df, avg_ratings, on="ISBN", how="left")
books_df["est_rating"] = books_df["est_rating"].fillna(0).round(2)

# Ana sayfa
@app.get("/")
def read_root():
    return {
        "message": "Hoş geldiniz! Kitap API'si çalışıyor.",
        "sample_books": books_df.head(500).to_dict(orient="records")
    }

# Öneri endpointi
@app.get("/recommend/{book_title}")
def recommend(book_title: str):
    matched = books_df[books_df["Title"].str.contains(book_title, case=False, na=False)].copy()
    if matched.empty:
        return {"error": "Kitap bulunamadı."}
    results = matched.sort_values("est_rating", ascending=False).head(5)
    return {"recommendations": results[["Title", "est_rating"]].to_dict(orient="records")}

# Arama endpointi
@app.get("/search")
def search_books(q: str = Query(..., min_length=1)):
    matched = books_df[books_df["Title"].str.contains(q, case=False, na=False)].copy()
    return matched[["Title", "est_rating"]].head(20).to_dict(orient="records")

# Örnek kitaplar
@app.get("/sample_books")
def get_sample_books():
    return books_df.head(1000).to_dict(orient="records")

