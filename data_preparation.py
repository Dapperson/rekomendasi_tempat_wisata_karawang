import pandas as pd
<<<<<<< HEAD:data_preparation.py
# import os

# data_folder = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'data'))

# data_user_combined = pd.read_excel(os.path.join(data_folder, 'data_user_combined.xlsx'))
# combined_place_data = pd.read_excel(os.path.join(data_folder, 'combined_place_data.xlsx'))

data_user_combined = pd.read_csv('.\data\data_user_combined_v2.csv')
combined_place_data = pd.read_csv('.\data\combined_place_data_v2.csv')
=======

data_user_combined = pd.read_csv('..\data\data_user_combined_v2.csv')
combined_place_data = pd.read_csv('..\data\combined_place_data_v2.csv')
>>>>>>> 778867cbffc22e67908a2ff040d534aa799e2da6:notebook/data_preparation.py

new_data_user = data_user_combined.copy()
new_data_place = combined_place_data.copy()

new_data_user.rename(columns={'Email Address':'email',
                               'Nama':'nama_pengguna',
                               'Usia':'usia',
                               'Status':'status',
                               'Tempat Tinggal (Kota/Kabupaten)':'tempat_tinggal',
                               'Rating':'rating',
                               'Nama Tempat Wisata':'nama_tempat',
                               'Kecamatan':'kecamatan',
                               'Kategori':'kategori',
                               'ID Tempat':'id_tempat'}, inplace=True)

new_data_place.rename(columns={'ID Tempat':'id_tempat',
                                'Nama Tempat Wisata': 'nama_tempat',
                                'Kecamatan': 'kecamatan',
                                'Kategori': 'kategori',
                                'city': 'kota',
                                'reviewsCount': 'jumlah_ulasan',
                                'Address': 'alamat',
                                'postalCode': 'kode_pos',
                                'phone': 'telepon',
                                'location/lat': 'latitude',
                                'location/lng': 'longitude'}, inplace=True)
