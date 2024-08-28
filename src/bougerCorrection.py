import pandas as pd
import numpy as np

def koreksi_bouguer(file_input, file_output):

    
    # Baca file input
    data = pd.read_csv(file_input)
    
    # Pastikan kolom yang diperlukan ada
    kolom_wajib = ['height', 'g', 'tidal_correction', 'latitude_correction', 'free_air_correction', 'terrain_correction']
    if not all(col in data.columns for col in kolom_wajib):
        raise ValueError("File input harus memiliki kolom: height, g, tidal_correction, latitude_correction, free_air_correction, dan terrain_correction")
    
    # Konstanta untuk koreksi Bouguer
    densitas_rata_rata_kerak = 2.67  # g/cm^3
    konstanta_gravitasi = 6.67430e-11  # m^3 kg^-1 s^-2
    
    # Hitung koreksi Bouguer
    data['koreksi_bouguer'] = 2 * np.pi * konstanta_gravitasi * densitas_rata_rata_kerak * 100 * data['height'] * 1e-5  # dalam mGal
    
    # Hitung anomali Bouguer lengkap
    # data['anomali_bouguer'] = (data['g'] + 
    #                            data['tidal_correction'] + 
    #                            data['latitude_correction'] + 
    #                            data['free_air_correction'] + 
    #                            data['terrain_correction'] - 
    #                            data['koreksi_bouguer'])
    
    data['anomali_bouger'] = ((data['g']- 6.67430e-11) + (data['tidal_correction'] + 
    data['latitude_correction'] + 
    data['free_air_correction'] + 
    data['terrain_correction'] - 
    data['koreksi_bouguer']))
    
    # Simpan hasil ke file output
    data.to_csv(file_output, index=False)
    
    print(f"Koreksi Bouguer telah selesai. Hasil disimpan di {file_output}")


def koreksi_bouguer_tanpa_tidal(file_input, file_output):
    # Baca file input
    data = pd.read_csv(file_input)
    
    # Pastikan kolom yang diperlukan ada
    kolom_wajib = ['height', 'g', 'latitude_correction', 'free_air_correction', 'terrain_correction']
    if not all(col in data.columns for col in kolom_wajib):
        raise ValueError("File input harus memiliki kolom: height, g, latitude_correction, free_air_correction, dan terrain_correction")
    
    # Konstanta untuk koreksi Bouguer
    densitas_rata_rata_kerak = 2.67  # g/cm^3
    konstanta_gravitasi = 6.67430e-11  # m^3 kg^-1 s^-2
    
    # Hitung koreksi Bouguer
    data['koreksi_bouguer'] = 2 * np.pi * konstanta_gravitasi * densitas_rata_rata_kerak * 100 * data['height'] * 1e-5  # dalam mGal
    
    # Hitung anomali Bouguer lengkap tanpa data pasang surut
    data['anomali_bouger'] = ((data['g'] - 6.67430e-11) + 
                              data['latitude_correction'] + 
                              data['free_air_correction'] + 
                              data['terrain_correction'] - 
                              data['koreksi_bouguer'])
    
    # Simpan hasil ke file output
    data.to_csv(file_output, index=False)
    
    print(f"Koreksi Bouguer tanpa data pasang surut telah selesai. Hasil disimpan di {file_output}")

# Fungsi untuk memilih metode koreksi Bouguer yang sesuai
def pilih_koreksi_bouguer(file_input, file_output):
    data = pd.read_csv(file_input)
    
    if 'tidal_correction' in data.columns:
        print("Menggunakan metode koreksi Bouguer dengan data pasang surut")
        return koreksi_bouguer(file_input, file_output)
    else:
        print("Menggunakan metode koreksi Bouguer tanpa data pasang surut")
        return koreksi_bouguer_tanpa_tidal(file_input, file_output)

# Contoh penggunaan:
# if __name__ == "__main__":
#     file_input = "/home/sat/diki/gravity/Gravity/data/data_with_terrain_correction.csv"
#     file_output = "/home/sat/diki/gravity/Gravity/data/data_with_bouguer_correction.csv"
#     koreksi_bouguer(file_input, file_output)
