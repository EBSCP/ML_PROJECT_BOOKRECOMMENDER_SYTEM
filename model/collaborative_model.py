from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

def train_svd_model(ratings_df):
    reader = Reader(rating_scale=(0, 10))  # çünkü Rating 0-10 arası
    data = Dataset.load_from_df(ratings_df[['user_id', 'isbn', 'rating']], reader)
    trainset, _ = train_test_split(data, test_size=0.2)
    model = SVD()
    model.fit(trainset)
    return model
