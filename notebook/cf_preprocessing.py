import numpy as np
from data_preparation import new_data_user

user_email = new_data_user['email'].unique().tolist()
user_to_user_encoded = {x: i for i, x in enumerate(user_email)}
user_encoded_to_user = {i: x for i, x in enumerate(user_email)}

place_ids = new_data_user['id_tempat'].unique().tolist()
place_to_place_encoded = {x: i for i, x in enumerate(place_ids)}
place_encoded_to_place = {i: x for i, x in enumerate(place_ids)}

new_data_user['user'] = new_data_user['email'].map(user_to_user_encoded)
new_data_user['place'] = new_data_user['id_tempat'].map(place_to_place_encoded)

num_users = len(user_to_user_encoded)
num_place = len(place_encoded_to_place)
new_data_user['rating'] = new_data_user['rating'].values.astype(np.float32)
min_rating = min(new_data_user['rating'])
max_rating = max(new_data_user['rating'])
