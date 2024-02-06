import os
import pandas as pd

# Mendefinisikan path ke folder data
data_folder = 'data'

# Memuat data pengguna gabungan
data_user_combined_path = os.path.join(data_folder, 'data_user_combined.xlsx')
data_user_combined = pd.read_excel(data_user_combined_path)

# Memuat data tempat gabungan
combined_place_data_path = os.path.join(data_folder, 'combined_place_data.xlsx')
combined_place_data = pd.read_excel(combined_place_data_path)

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
