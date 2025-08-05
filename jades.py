import os
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.cosmology import Planck18
import astropy.units as u

# Step 1: Specify the folder path (replace with your actual folder path)
# folder_path = '/fits'  # Change this to your folder path
# If running in the same folder, use '.'
folder_path = '.'

# Step 2: Find only FITS files in the folder
fits_files = [f for f in os.listdir(folder_path) if f.endswith('.fits')]

# Step 3: Print the list of FITS files
print("FITS files in the folder:")
for file in fits_files:
    print(file)

# Step 4: Analyze each FITS file (optional loop)
for file in fits_files:
    full_path = os.path.join(folder_path, file)
    hdul = fits.open(full_path)
    print(f"Data from {file}: {hdul.info()}")  # Basic file info
    hdul.close()

# Extended analysis: Extract spectrum and calculate z, distance, tau for each file
plt.figure(figsize=(12, 8))

for file in fits_files:
    try:
        full_path = os.path.join(folder_path, file)
        hdul = fits.open(full_path)
        
        # Check if it's an x1d file (1D extracted spectrum)
        if 'x1d' in file:
            # For x1d files, data is in EXTRACT1D extensions as tables
            if len(hdul) > 1 and 'EXTRACT1D' in hdul[1].name:
                data = hdul[1].data
                if hasattr(data, 'dtype') and hasattr(data.dtype, 'names'):
                    # Check if WAVELENGTH and FLUX columns exist
                    if 'WAVELENGTH' in data.dtype.names and 'FLUX' in data.dtype.names:
                        wavelength = data['WAVELENGTH']
                        flux = data['FLUX']
                        
                        # Remove any NaN or invalid values
                        valid_mask = np.isfinite(wavelength) & np.isfinite(flux) & (flux != 0)
                        wavelength = wavelength[valid_mask]
                        flux = flux[valid_mask]
                        
                        if len(wavelength) > 0:
                            # Calculate z from Lyman-alpha line (approximate)
                            lyman_rest = 0.1216  # microns (rest wavelength of Lyman-alpha)
                            # Find the peak in the spectrum as a rough estimate
                            peak_idx = np.argmax(flux)
                            lyman_obs = wavelength[peak_idx]  # microns (observed wavelength)
                            z = (lyman_obs / lyman_rest) - 1
                            
                            print(f"File {file}: Calculated redshift z = {z:.2f}")
                            
                            # Calculate luminosity distance (x)
                            distance = Planck18.luminosity_distance(z)
                            x_mpc = distance.to(u.Mpc).value
                            x_m = distance.to(u.m).value
                            print(f"Distance: {x_mpc:.2f} Mpc")
                            
                            # Calculate tau (from model: tau ≈ k * x / c)
                            c = 3e8  # m/s (speed of light)
                            k = 0.05  # Small constant (estimate; adjust to fit data)
                            tau = k * x_m / c  # in seconds
                            delta_z = tau * c / x_m  # Approximate delta_z
                            print(f"Tau (time delay): {tau:.2e} s")
                            print(f"Delta_z (redshift shift): {delta_z:.2f}")
                            
                            # Plot the spectrum
                            plt.plot(wavelength, flux, label=f"{file} (z={z:.2f})", alpha=0.7)
                        else:
                            print(f"File {file}: No valid data points found")
                    else:
                        print(f"File {file}: Missing WAVELENGTH or FLUX columns")
                else:
                    print(f"File {file}: Data is not in expected table format")
            else:
                print(f"File {file}: No EXTRACT1D extension found")
        
        # Check if it's an s2d file (2D spectral data)
        elif 's2d' in file:
            # For s2d files, data is in SCI extensions as 2D arrays
            if len(hdul) > 1 and 'SCI' in hdul[1].name:
                # Get the first SCI extension
                sci_data = hdul[1].data
                wavelength_data = hdul[3].data  # WAVELENGTH extension
                
                if sci_data is not None and wavelength_data is not None:
                    # Extract a 1D spectrum by averaging along the spatial axis
                    # Take the middle row as a simple extraction
                    middle_row = sci_data.shape[0] // 2
                    flux_1d = sci_data[middle_row, :]
                    wavelength_1d = wavelength_data[middle_row, :]
                    
                    # Remove any NaN or invalid values
                    valid_mask = np.isfinite(wavelength_1d) & np.isfinite(flux_1d) & (flux_1d != 0)
                    wavelength_1d = wavelength_1d[valid_mask]
                    flux_1d = flux_1d[valid_mask]
                    
                    if len(wavelength_1d) > 0:
                        # Calculate z from Lyman-alpha line (approximate)
                        lyman_rest = 0.1216  # microns
                        peak_idx = np.argmax(flux_1d)
                        lyman_obs = wavelength_1d[peak_idx]
                        z = (lyman_obs / lyman_rest) - 1
                        
                        print(f"File {file}: Calculated redshift z = {z:.2f}")
                        
                        # Calculate luminosity distance (x)
                        distance = Planck18.luminosity_distance(z)
                        x_mpc = distance.to(u.Mpc).value
                        x_m = distance.to(u.m).value
                        print(f"Distance: {x_mpc:.2f} Mpc")
                        
                        # Calculate tau
                        c = 3e8  # m/s
                        k = 0.05
                        tau = k * x_m / c
                        delta_z = tau * c / x_m
                        print(f"Tau (time delay): {tau:.2e} s")
                        print(f"Delta_z (redshift shift): {delta_z:.2f}")
                        
                        # Plot the spectrum
                        plt.plot(wavelength_1d, flux_1d, label=f"{file} (z={z:.2f})", alpha=0.7)
                    else:
                        print(f"File {file}: No valid data points found")
                else:
                    print(f"File {file}: No valid SCI or WAVELENGTH data")
            else:
                print(f"File {file}: No SCI extension found")
        
        else:
            print(f"File {file}: Unknown file type (not x1d or s2d)")
        
        hdul.close()
        
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")
        try:
            hdul.close()
        except:
            pass

plt.xlabel('Wavelength (microns)')
plt.ylabel('Flux')
plt.title('JADES-GS-z14-0 Spectra')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(True, alpha=0.3)
plt.show()