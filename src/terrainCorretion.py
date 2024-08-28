
import numpy as np
import pandas as pd

def terrain_correction(input_file, output_file):

    # Baca file input
    data = pd.read_csv(input_file)
    
    # Pastikan kolom yang diperlukan ada
    required_columns = ['tidal_correction', 'free_air_correction', 'latitude_correction']
    if not all(col in data.columns for col in required_columns):
        raise ValueError("File input harus memiliki kolom: tidal_correction, free_air_correction, dan latitude_correction")
    
    # Konstanta untuk koreksi terrain
    terrain_constant = 0.3086  # mGal/m
    
    # Hitung koreksi terrain
    # Asumsi: efek terrain proporsional terhadap elevasi (menggunakan tidal_correction sebagai proxy untuk elevasi)
    data['terrain_correction'] = terrain_constant * data['tidal_correction']
    
    
    # Simpan hasil ke file output
    return data.to_csv(output_file, index=False)

def terrain_correction_without_tidal(input_file, output_file):
    # Baca file input
    data = pd.read_csv(input_file)
    
    # Pastikan kolom yang diperlukan ada
    required_columns = ['height', 'free_air_correction', 'latitude_correction']
    if not all(col in data.columns for col in required_columns):
        raise ValueError("File input harus memiliki kolom: height, free_air_correction, dan latitude_correction")
    
    # Konstanta untuk koreksi terrain
    terrain_constant = 0.3086  # mGal/m
    
    # Hitung koreksi terrain menggunakan kolom 'height' sebagai pengganti 'tidal_correction'
    data['terrain_correction'] = terrain_constant * data['height']
    
    # Simpan hasil ke file output
    return data.to_csv(output_file, index=False)

# Fungsi untuk memilih metode koreksi terrain yang sesuai
def choose_terrain_correction(input_file, output_file):
    data = pd.read_csv(input_file)
    
    if 'tidal_correction' in data.columns:
        print("Menggunakan metode koreksi terrain dengan data pasang surut")
        return terrain_correction(input_file, output_file)
    else:
        print("Menggunakan metode koreksi terrain tanpa data pasang surut")
        return terrain_correction_without_tidal(input_file, output_file)

    
    

# Contoh penggunaan:
# if __name__ == "__main__":
#     input_file = "/home/sat/diki/gravity/Gravity/data/data_with_free_air_correction.csv"
#     output_file = "/home/sat/diki/gravity/Gravity/data/data_with_terrain_correction.csv"
#     terrain_correction(input_file, output_file)
