import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
import os
from cb_preprocessing import cosine_sim_df, place_new
from cf_preprocessing import new_data_place, new_data_user, user_email, place_to_place_encoded, user_to_user_encoded, place_encoded_to_place
from load_model import model

place_df = new_data_place
user_df = new_data_user

place_name_list = place_df['nama_tempat'].to_list()

def tempat_recommendations(nama_tempat, similarity_data=cosine_sim_df,
                           items=place_new[['id_tempat','nama_tempat', 'kategori', 'rating', 'jumlah_ulasan', 'kecamatan', 'alamat', 'url']], k=30):
    if nama_tempat not in similarity_data.columns:
        st.error("Nama Tempat Wisata tidak diketahui, berikut beberapa rekomendasi Tempat Wisata yang ada:")
        random_recommendations = items[items['rating'] > 4].sample(20).reset_index(drop=True)
        random_recommendations.index += 1
        return random_recommendations
    else:
        st.write("Berikut beberapa rekomendasi Tempat Wisata yang Relavan dengan Tempat Tersebut:")
        index = similarity_data.loc[:,nama_tempat].to_numpy().argpartition(
            range(-1, -k, -1))
        closest = similarity_data.columns[index[-1:-(k+2):-1]]
        closest = closest.drop(nama_tempat, errors='ignore')
        recommendations = pd.DataFrame(closest).merge(items)
        recommendations.reset_index(drop=True, inplace=True)
        recommendations.index += 1
        for row in recommendations.itertuples():
            st.divider()
            col1, col2, col3 = st.columns([0.2, 1.5, 2])
            with col1:
                st.write(row.Index)
            with col2:
                place_path = f"./pictures/{row.id_tempat}.jpg"
                if os.path.exists(place_path):
                    image = Image.open(place_path)
                else:
                    image = Image.open("./pictures/default.png")
                image = ImageOps.fit(image, (250, 250))
                st.image(image, width=250)
            with col3:
                st.write("Nama Tempat :",row.nama_tempat)
                st.write("Kategori :",row.kategori)
                st.write("Rating\t:",row.rating)
                st.write("Jumlah Ulasan :",row.jumlah_ulasan)
                st.write("Kecamatan :",row.kecamatan)
                st.write("Alamat :",row.alamat)
            st.write("Link Google Maps:",row.url)

def show_recommendations_by_user_id(user_id):
    if user_id not in user_email:
        st.error("Email pengguna tidak ditemukan dalam data.")
        st.write("Menampilkan beberapa rekomendasi Tempat Wisata yang ada:")

        top_places = new_data_place[new_data_place['rating'] > 4].sample(30)
        top_places.reset_index(drop=True, inplace=True)
        top_places.index += 1
        for row in top_places.itertuples():
            st.divider()
            col1, col2, col3 = st.columns([0.2, 1.5, 2])
            with col1:
                st.write(row.Index)
            with col2:
                place_path = f"./pictures/{row.id_tempat}.jpg"
                if os.path.exists(place_path):
                    image = Image.open(place_path)
                else:
                    image = Image.open("./pictures/default.png")
                image = ImageOps.fit(image, (250, 250))
                st.image(image, width=250)
            with col3:
                st.write("Nama Tempat :",row.nama_tempat)
                st.write("Kategori :",row.kategori)
                st.write("Rating\t:",row.rating)
                st.write("Jumlah Ulasan :",row.jumlah_ulasan)
                st.write("Kecamatan :",row.kecamatan)
                st.write("Alamat :",row.alamat)
            st.write("Link Google Maps:",row.url)

    else:
        place_visited_by_user = user_df[user_df['email'] == user_id]

        place_not_visited = place_df[~place_df['id_tempat'].isin(place_visited_by_user['id_tempat'])]['id_tempat']
        place_not_visited = list(set(place_not_visited).intersection(set(place_to_place_encoded.keys())))
        place_not_visited_encoded = [place_to_place_encoded.get(x) for x in place_not_visited]

        place_not_visited = [[place_to_place_encoded.get(x)] for x in place_not_visited]
        user_encoder = user_to_user_encoded.get(user_id)
        user_place_array = [
            np.array([[user_encoder]] * len(place_not_visited_encoded)),
            np.array(place_not_visited_encoded),
            np.array([[user_encoder]] * len(place_not_visited_encoded)),
            np.array(place_not_visited_encoded)
        ]

        ratings = model.predict(user_place_array).flatten()

        top_ratings_indices = ratings.argsort()[-30:][::-1]
        recommended_place_ids = [
            place_encoded_to_place.get(place_not_visited[x][0]) for x in top_ratings_indices
        ]

        st.write('Menampilkan Rekomendasi untuk Pengguna dengan email: {}'.format(user_id))
        st.subheader('Tempat Wisata yang mungkin cocok untuk pengguna')

        top_place_user = (
            place_visited_by_user.sort_values(
                by='rating',
                ascending=False
            )
            .head(10)['id_tempat'].values
        )

        place_df_rows = place_df[place_df['id_tempat'].isin(top_place_user)]
        place_df_rows.reset_index(drop=True, inplace=True)
        place_df_rows.index += 1
        if not place_df_rows.empty:
            for row in place_df_rows.itertuples():
                st.divider()
                col1, col2, col3 = st.columns([0.2, 1.5, 2])
                with col1:
                    st.write(row.Index)
                with col2:
                    place_path = f"./pictures/{row.id_tempat}.jpg"
                    if os.path.exists(place_path):
                        image = Image.open(place_path)
                    else:
                        image = Image.open("./pictures/default.png")
                    image = ImageOps.fit(image, (250, 250))
                    st.image(image, width=250)
                with col3:
                    st.write("Nama Tempat :",row.nama_tempat)
                    st.write("Kategori :",row.kategori)
                    st.write("Rating\t:",row.rating)
                    st.write("Jumlah Ulasan :",row.jumlah_ulasan)
                    st.write("Kecamatan :",row.kecamatan)
                    st.write("Alamat :",row.alamat)
                st.write("Link Google Maps:",row.url)
        else:
            st.write("Tidak ada rekomendasi untuk tempat wisata yang dikunjungi oleh pengguna.")

        st.divider()
        st.subheader('Rekomendasi Tempat Wisata dari Pengguna Lain')

        recommended_place = place_df[place_df['id_tempat'].isin(recommended_place_ids)]
        recommended_place = recommended_place.dropna(subset=['rating'])
        recommended_place.reset_index(drop=True, inplace=True)
        recommended_place.index += 1
        if not recommended_place.empty:
            for row in recommended_place.itertuples():
                st.divider()
                col1, col2, col3 = st.columns([0.2, 1.5, 2])
                with col1:
                    st.write(row.Index)
                with col2:
                    place_path = f"./pictures/{row.id_tempat}.jpg"
                    if os.path.exists(place_path):
                        image = Image.open(place_path)
                    else:
                        image = Image.open("./pictures/default.png")
                    image = ImageOps.fit(image, (250, 250))
                    st.image(image, width=250)
                with col3:
                    st.write("Nama Tempat :",row.nama_tempat)
                    st.write("Kategori :",row.kategori)
                    st.write("Rating\t:",row.rating)
                    st.write("Jumlah Ulasan :",row.jumlah_ulasan)
                    st.write("Kecamatan :",row.kecamatan)
                    st.write("Alamat :",row.alamat)
                st.write("Link Google Maps:",row.url)
            
        else:
            st.write("Tidak ada rekomendasi tempat wisata dari pengguna lain.")


def explore_places(place_df):
    st.header('Eksplor Tempat Wisata 🗺️')

    # Filter berdasarkan nama tempat
    place_name_filter = st.text_input('Filter berdasarkan nama tempat:')
    filtered_places = place_df[place_df['nama_tempat'].str.contains(place_name_filter, case=False)]

    # Filter berdasarkan kategori
    categories = place_df['kategori'].unique()
    selected_category = st.selectbox('Filter berdasarkan kategori:', ['Semua'] + list(categories))
    if selected_category != 'Semua':
        filtered_places = filtered_places[filtered_places['kategori'] == selected_category]

    # Filter berdasarkan kecamatan
    districts = place_df['kecamatan'].unique()
    selected_district = st.selectbox('Filter berdasarkan kecamatan:', ['Semua'] + list(districts))
    if selected_district != 'Semua':
        filtered_places = filtered_places[filtered_places['kecamatan'] == selected_district]

    # Filter berdasarkan rating
    min_rating = st.slider('Filter minimal rating:', min_value=0.0, max_value=5.0, step=0.5, value=0.0)
    filtered_places = filtered_places[filtered_places['rating'] >= min_rating]

    # Filter berdasarkan jumlah ulasan
    min_reviews = st.slider('Filter minimal jumlah ulasan:', min_value=0, max_value=1000, step=10, value=0)
    filtered_places = filtered_places[filtered_places['jumlah_ulasan'] >= min_reviews]

    # Tampilkan hasil filter
    st.divider()
    st.subheader('Hasil Filter:')
    if filtered_places.empty:
        st.error('Tidak ada tempat wisata yang cocok dengan filter yang diberikan.')
    else:
        filtered_places.reset_index(drop=True, inplace=True)
        filtered_places.index += 1
        st.dataframe(filtered_places)
        if not filtered_places.empty:
            for row in filtered_places.itertuples():
                st.divider()
                col1, col2, col3 = st.columns([0.3, 1.5, 2])
                with col1:
                    st.write(row.Index)
                with col2:
                    place_path = f"./pictures/{row.id_tempat}.jpg"
                    if os.path.exists(place_path):
                        image = Image.open(place_path)
                    else:
                        image = Image.open("./pictures/default.png")
                    image = ImageOps.fit(image, (250, 250))
                    st.image(image, width=250)
                with col3:
                    st.write("Nama Tempat :",row.nama_tempat)
                    st.write("Kategori :",row.kategori)
                    st.write("Rating\t:",row.rating)
                    st.write("Jumlah Ulasan :",row.jumlah_ulasan)
                    st.write("Kecamatan :",row.kecamatan)
                    st.write("Alamat :",row.alamat)
                st.write("Link Google Maps:",row.url)