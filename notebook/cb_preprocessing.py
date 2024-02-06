import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_preparation import new_data_place, new_data_user

def preprocess_data():
    preparation = new_data_user.drop_duplicates('id_tempat')
    
    place_id = preparation['id_tempat'].tolist()
    place_name = preparation['nama_tempat'].tolist()
    place_categories = preparation['kategori'].tolist()
    
    place_new = pd.DataFrame({
    'id_tempat': place_id,
    'nama_tempat': place_name,
    'kategori': place_categories
    })

    place_new = pd.merge(place_new, new_data_place[['nama_tempat', 'kecamatan', 'rating', 'jumlah_ulasan', 'alamat', 'url']], on='nama_tempat', how='left')

    tf = TfidfVectorizer()
    tfidf_matrix = tf.fit_transform(place_new['kategori'])

    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, place_new['nama_tempat'], columns=place_new['nama_tempat'])

    return cosine_sim_df, place_new

cosine_sim_df, place_new = preprocess_data()
