from tensorflow import keras
import os

# Mendefinisikan path ke folder model
model_folder = 'model'

# Memuat model
model_path = os.path.join(model_folder, 'sr_wisata_karawang_v1.h5')
model = keras.models.load_model(model_path)