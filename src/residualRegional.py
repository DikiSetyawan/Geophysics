import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

def hitung_residual_regional(file_input, file_output):

    # Baca file input
    data = pd.read_csv(file_input)
    
    # Pastikan kolom yang diperlukan ada
    if 'anomali_bouger' not in data.columns:
        raise ValueError("File input harus memiliki kolom 'anomali_bouger'")
    
    # Hitung ukuran grid yang sesuai dengan jumlah data
    grid_size = int(np.ceil(np.sqrt(len(data))))
    
    # Ubah data menjadi grid 2D
    x = data['long'].values
    y = data['lat'].values
    z = data['anomali_bouger'].values
    
    # Buat grid reguler
    xi = np.linspace(x.min(), x.max(), grid_size)
    yi = np.linspace(y.min(), y.max(), grid_size)
    xi, yi = np.meshgrid(xi, yi)
    
    # Interpolasi data ke grid reguler
    zi = griddata((x, y), z, (xi, yi), method='linear')
    
    # Hitung peta regional menggunakan filter low-pass
    kernel_size = 5  # Ukuran kernel, bisa disesuaikan
    regional = signal.medfilt2d(zi, kernel_size=kernel_size)
    
    # Hitung peta residual
    residual = zi - regional
    
    # Interpolasi kembali ke posisi data asli
    regional_interp = griddata((xi.ravel(), yi.ravel()), regional.ravel(), (x, y), method='linear')
    residual_interp = griddata((xi.ravel(), yi.ravel()), residual.ravel(), (x, y), method='linear')
    
    # Tambahkan hasil ke DataFrame
    data['regional'] = regional_interp
    data['residual'] = residual_interp
    
    # Simpan hasil ke file output
    data.to_csv(file_output, index=False)
    
    print(f"Perhitungan peta residual dan regional telah selesai. Hasil disimpan di {file_output}")


# def hitung_residual_regional(file_input, file_output):
#     data = pd.read_csv(file_input)
#     x = data['long'].unique()
#     y = data['lat'].unique()
#     z = data['anomali_bouger'].values


def buat_peta(file_input, kolom, file_output, is_residual=True):
    data = pd.read_csv(file_input)
    
    # Membuat grid untuk interpolasi
    x = np.linspace(data['long'].min(), data['long'].max(), 1000)
    y = np.linspace(data['lat'].min(), data['lat'].max(), 1000)
    X, Y = np.meshgrid(x, y)
    
    # Interpolasi data
    Z = griddata((data['long'], data['lat']), data[kolom], (X, Y), method='linear')
    
    print(f"Min value: {data[kolom].min()}, Max value: {data[kolom].max()}")
    
    print(f"Z shape: {Z.shape}, Z min: {np.nanmin(Z)}, Z max: {np.nanmax(Z)}")
    
    plt.figure(figsize=(12, 8))
    im = plt.imshow(Z, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                    origin='lower', cmap='coolwarm', aspect='auto')
    plt.colorbar(im, label=kolom)
    plt.title(f'Peta {kolom.capitalize()}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(file_output, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Peta {kolom} telah disimpan di {file_output}")

    print("Peta residual dan regional telah disimpan.")

# if __name__ == "__main__":
#     file_input = "./data/hasil_koreksi_gravitasi_lengkap.csv"
#     file_output = "./data/hasil_residual_regional.csv"
#     hitung_residual_regional(file_input, file_output)
