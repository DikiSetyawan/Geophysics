import pandas as pd
import numpy as np

def free_air_correction(height):
    # Konstanta koreksi udara bebas dalam mGal/m
    FAC_CONSTANT = 0.3086
    
    # Hitung koreksi udara bebas
    correction = FAC_CONSTANT * height
    
    return correction

def process_free_air_correction(file_path):
    data = pd.read_csv(file_path)
    if 'height' not in data.columns:
        raise ValueError("Kolom 'height' tidak ditemukan dalam data")
    
    # Hitung koreksi udara bebas untuk setiap baris data
    data['free_air_correction'] = data['height'].apply(free_air_correction)
    
    return data.to_csv(file_path, index=False)

# if __name__ == "__main__":
#     # Baca file input CSV
#     input_file = "/home/sat/diki/gravity/Gravity/data/data_with_latitude_correction.csv"
#     data = pd.read_csv(input_file)
    
#     # Proses koreksi udara bebas
#     corrected_data = process_free_air_correction(data)
    
#     # Simpan hasil ke file output CSV
#     output_file = "/home/sat/diki/gravity/Gravity/data/data_with_free_air_correction.csv"
#     corrected_data.to_csv(output_file, index=False)
    
#     print("Koreksi udara bebas telah dihitung dan disimpan di", output_file)
#     print("Beberapa baris pertama dari hasil:")
#     print(corrected_data.head())
