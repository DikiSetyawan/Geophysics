import pandas as pd
import matplotlib.pyplot as plt

def plot_raw_gravity(file_path):
    data = pd.read_csv(file_path)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(data['long'], data['lat'], c=data['g'], cmap='coolwarm')
    plt.colorbar(scatter, label='Gravity (mGal)')
    plt.title('Raw Gravity Data')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig('raw_gravity_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Plot data gravitasi mentah telah disimpan.")

# Gunakan fungsi ini dengan file data mentah Anda
plot_raw_gravity('/home/sat/diki/gravity/Gravity/data/data_gravitasi.csv')