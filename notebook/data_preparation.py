import pandas as pd

data_user_combined = pd.read_excel('data_user_combined.xlsx')
combined_place_data = pd.read_excel('combined_place_data.xlsx')

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
