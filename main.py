import pandas as pd
from src.tidalCorrection import tidal_correction
from src.latitudeCorrection import process_latitude_correction
from src.FaaCorrection import process_free_air_correction
from src.terrainCorretion import *
from src.bougerCorrection import *
from src.residualRegional import hitung_residual_regional, buat_peta

def proses_koreksi_gravitasi(file_input, file_output):
    # Langkah 1: Koreksi Pasang Surut
    data = tidal_correction(file_input)
    
    # Langkah 2: Koreksi Lintang
    data = process_latitude_correction(file_input)
    if data is None:
        print("Error: data adalah None setelah koreksi lintang")
        return
    
    # Langkah 3: Koreksi Udara Bebas
    data = process_free_air_correction(data)
    
    # Langkah 4: Koreksi Terrain
    data = terrain_correction(data)
    
    # Langkah 5: Koreksi Bouguer
    data = koreksi_bouguer(data, file_output)
    
    print(f"Semua koreksi gravitasi telah selesai. Hasil akhir disimpan di {file_output}")
    return data

def gravity_processing1(file_output):
    # tidal_correction(file_input, file_output)
    process_latitude_correction(file_output)
    process_free_air_correction(file_output)
    print('data preprocessing done')
    

def gravity_processing2(file_input, file_output):
    if 'tidal_correction' in file_input:    
        terrain_correction(file_input, file_output)
    else:
        terrain_correction_without_tidal(file_input, file_output)
    #koreksi_bouguer(file_input, file_output)
    print('data preprocessing2 done')

def gravity_processing3(file_input, file_output):
    if 'tidal_correction' in file_input:    
        koreksi_bouguer(file_input, file_output)
    else:
        koreksi_bouguer_tanpa_tidal(file_input, file_output)
    print('data preprocessing3 done')



# Langkah 6: Hitung Residual dan Regional
def proses_residual_regional(file_input, file_output):
    return hitung_residual_regional(file_input, file_output)

# Contoh penggunaan:
file_input = "./data/tes.csv"
tidal_data = "./data/hasil_akhir.csv"
data_terrain = "./data/data_with_terrain_correction.csv"
data_bouguer = "./data/data_with_bouguer_correction.csv"
data_residual = "./data/data_with_residual_regional.csv"

gravity_processing1(file_input)
gravity_processing2(file_input, data_terrain)
gravity_processing3(data_terrain, data_bouguer)
proses_residual_regional(data_bouguer, data_residual)
buat_peta(data_residual, 'residual', './data/peta_residual.png')
buat_peta(data_residual, 'regional', './data/peta_regional.png', is_residual=False)
# data = proses_koreksi_gravitasi(file_input, file_output)
# data = hitung_cba(data)
# proses_residual_regional(file_output, file_output)

# data = pd.read_csv(file_output)
# buat_peta(file_output, 'residual', './data/peta_residual.png')
# buat_peta(file_output, 'regional', './data/peta_regional.png', is_residual=False)

# print("Semua proses telah selesai.")
