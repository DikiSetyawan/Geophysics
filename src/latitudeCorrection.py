import numpy as np
import pandas as pd
# Constants for theoretical gravity formula
a = 978032.7  # theoretical gravity value at the equator (mGal)
b = 0.005172  # constant for sin^2(lat) term
c = -0.000007 # constant for sin^2(2lat) term

def latitude_correction(latitude, g_observed):

    
    # Convert latitude to radians
    lat_rad = np.radians(latitude)
    
    # Calculate theoretical gravity using international formula
    g_theoretical = a * (1 + b * np.sin(lat_rad)**2 + c * np.sin(2*lat_rad)**2)
    
    # Calculate latitude correction
    correction = g_observed - g_theoretical
    
    return correction

def process_latitude_correction(file_path):
    # Pastikan data dibaca sebagai DataFrame
    data = pd.read_csv(file_path)
    

    
    data['latitude_correction'] = data.apply(lambda row: latitude_correction(row['lat'], row['g']), axis=1)
    return data.to_csv(file_path, index=False)
    


# Example usage:
# if __name__ == "__main__":
#     # Read CSV file
#     input_file = "/home/sat/diki/gravity/Gravity/data/output_data_with_tidal_correction.csv"
#     data = pd.read_csv(input_file)
    
#     # Process latitude correction
#     corrected_data = process_latitude_correction(data)
    
#     # Save results to a new file
#     output_file = "/home/sat/diki/gravity/Gravity/data/data_with_latitude_correction.csv"
#     corrected_data.to_csv(output_file, index=False)
    
#     print("Latitude correction has been calculated and saved to", output_file)
#     print("First few rows of the result:")
#     print(corrected_data.head())

