def hybrid_recommendations(user_id, book_title, books_df, cosine_sim, indices, svd_model, top_n=10):
    # 1. İçerik tabanlı önerileri al
    idx = indices.get(book_title)
    if idx is None:
        return {"error": "Kitap bulunamadı."}

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    book_indices = [i[0] for i in sim_scores]

    # 2. Önerilen kitaplara SVD modeline göre puan tahmini yap
    hybrid_recs = []
    for i in book_indices:
        book = books_df.iloc[i]
        try:
            rating_pred = svd_model.predict(user_id, book['isbn']).est
        except:
            rating_pred = 0.0
        hybrid_recs.append({
            "title": book['title'],
            "predicted_rating": round(rating_pred, 2)
        })

    return hybrid_recs
