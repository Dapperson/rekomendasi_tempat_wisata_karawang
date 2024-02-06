import streamlit as st
from hybrid_recommendation import tempat_recommendations, show_recommendations_by_user_id, explore_places, place_name_list
from data_preparation import new_data_place
from PIL import Image
import streamlit.components.v1 as components

data_tempat_wisata = new_data_place.drop(columns=['id_tempat'])
data_tempat_wisata.index += 1

# Menambahkan tombol kembali ke atas
def back_to_top():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("[Kembali ke atas ⬆️](#top)")

# Fungsi untuk menampilkan link GitHub di sidebar
def display_github_link():
    github_link = "[![GitHub](https://img.shields.io/badge/GitHub-Dapperson-blue?logo=GitHub)](https://github.com/Dapperson)"
    st.markdown(github_link, unsafe_allow_html=True)

# Fungsi untuk menampilkan link LinkedIn di sidebar
def display_linkedin_link():
    linkedin_link = "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Roni_Merdi-blue?logo=LinkedIn)](https://www.linkedin.com/in/ronimerdi/)"
    st.markdown(linkedin_link, unsafe_allow_html=True)

menu = ['Beranda', 'Eksplor Tempat Wisata', 'Berdasarkan Tempat', 'Berdasarkan Pengguna', 'Tentang']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Eksplor Tempat Wisata':
    explore_places(new_data_place)

elif choice == 'Beranda':
    
    # Mengatur layout dengan menggunakan kolom
    col1, col2 = st.columns([2, 3])  # Mendefinisikan rasio lebar kolom
    
    # Menampilkan gambar di kolom pertama
    with col1:
        logo_path = "../pictures/logo_karawang.png"
        image = Image.open(logo_path)
        st.image(image, width=200)  # Mengatur lebar gambar menjadi 200 piksel

    # Menampilkan judul dan subjudul di kolom kedua
    with col2:
        st.title('Sistem Rekomendasi Tempat Wisata di Karawang')
        st.subheader('Selamat Datang')
        st.write('Silakan pilih menu untuk melanjutkan')

    # Menampilkan peta Google Maps
    st.divider()
    st.subheader('Peta Karawang')
    st.write('Silakan zoom out untuk menjelajahi area Karawang 🔍')
    components.html(
        """
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3960.0511206872673!2d107.03406431425691!3d-6.264703644530442!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69775e79e70e01%3A0x301576d14feb9e0!2sKarawang%2C%20West%20Java!5e0!3m2!1sen!2sid!4v1643990458016!5m2!1sen!2sid"
        width="800" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
        """,
        width=800,  # Mengatur lebar peta
        height=450,  # Mengatur tinggi peta
    )
    
    st.divider()
    st.subheader('Data Tempat Wisata Karawang 📍')
    st.dataframe(data_tempat_wisata)
    st.write('Sumber: Disparbud Karawang & Google Maps, Januari 2024')

elif choice == 'Berdasarkan Tempat':
    st.header('Berdasarkan Tempat 🏕️')
    place_name = st.selectbox('Pilih nama tempat', place_name_list, index=0)
    if st.button('Tampilkan Rekomendasi'):
        recommendations = tempat_recommendations(place_name)

elif choice == 'Berdasarkan Pengguna':
    st.header('Berdasarkan Pengguna 🧑🏻‍🌾')
    user_id = st.text_input('Masukkan email pengguna', 'abirafdimirza17@gmail.com')
    if st.button('Tampilkan Rekomendasi'):
        show_recommendations_by_user_id(user_id)

elif choice == 'Tentang':
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    col1, col2 = st.columns([2, 3])
    with col1:
        logo_path = "../pictures/programmer.png"
        image = Image.open(logo_path)
        st.image(image, width=300)
    with col2:
        st.write('')
        st.subheader('Jika anda ingin mengetahui lebih lanjut terkait Author maupun Project ini, silahkan hubungi melalui media dibawah ini 🎃')
        col3, col4 = st.columns([2, 2])
        with col3:
            display_linkedin_link()
        with col4:
            display_github_link()
        st.subheader('Let\'s Connected! ✨')