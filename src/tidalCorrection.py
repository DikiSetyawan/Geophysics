import numpy as np
from datetime import datetime
import pandas as pd


G = 6.67430e-11  # Konstanta gravitasi universal
M = 5.97e24  # Massa Bumi
R = 6371000  # Jari-jari rata-rata Bumi



def tidal_correction(input_file, output_file):
    # Baca file input CSV
    data = pd.read_csv(input_file)

    # Hitung koreksi pasang surut untuk setiap baris data
    tidal_values = np.array([longman_equation(row['time'], row['long'], row['lat'], row['g']) 
                             for _, row in data.iterrows()])

    # Tambahkan kolom baru untuk nilai koreksi pasang surut
    data['tidal_correction'] = tidal_values

    # Simpan hasil ke file output CSV
    return data.to_csv(output_file, index=False)

def longman_equation(time, lon, lat, g):
    # Konversi waktu ke format yang sesuai
    t = datetime.strptime(time, "%H:%M:%S")
    
    # Hitung sudut jam matahari
    hour_angle = 15 * (t.hour + t.minute / 60 + t.second / 3600 - 12)
    
    # Hitung deklinasi matahari (perkiraan sederhana)
    day_of_year = t.timetuple().tm_yday
    declination = 23.45 * np.sin(np.radians(360/365 * (284 + day_of_year)))
    
    # Hitung komponen vertikal pasang surut
    tidal_value = (G * M / R**2) * (3 * np.sin(np.radians(lat))**2 - 1) * \
                    (3 * np.sin(np.radians(declination))**2 - 1) / 2 + \
                    (G * M / R**2) * np.sin(2 * np.radians(lat)) * \
                    np.sin(2 * np.radians(declination)) * np.cos(np.radians(hour_angle))
    
    # Konversi ke mGal dan tambahkan ke nilai anomali gravitasi
    tidal_correction = tidal_value * 1e5 + g
    
    return tidal_correction

# Contoh penggunaan
# if __name__ == "__main__":
#     input_file = "/home/sat/diki/gravity/Gravity/data/data_gravitasi.csv"
#     output_file = "/home/sat/diki/gravity/Gravity/data/output_data_with_tidal_correction.csv"
#     result = tidal_correction(input_file, output_file)
#     print("Koreksi pasang surut telah dihitung dan disimpan di", output_file)
#     print("Beberapa baris pertama dari hasil:")
#     print(result.head())






