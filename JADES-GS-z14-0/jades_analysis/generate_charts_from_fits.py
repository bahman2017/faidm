
import os
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.cosmology import Planck18
import astropy.units as u

# Specify the folder path with FITS files
folder_path = 'data'

# Find only FITS files in the folder
fits_files = [f for f in os.listdir(folder_path) if f.endswith('.fits')]

print(f"Found {len(fits_files)} FITS files in {folder_path}/")

# Prepare a list to store results
results = []

# Step 1: Analyze each FITS file
for file in fits_files:
    try:
        full_path = os.path.join(folder_path, file)
        hdul = fits.open(full_path)

        # Check if it's an x1d file (1D extracted spectrum)
        if 'x1d' in file.lower():
            if len(hdul) > 1 and 'EXTRACT1D' in hdul[1].name:
                data = hdul[1].data
                if hasattr(data, 'dtype') and hasattr(data.dtype, 'names'):
                    if 'WAVELENGTH' in data.dtype.names and 'FLUX' in data.dtype.names:
                        wavelength = data['WAVELENGTH']
                        flux = data['FLUX']
                        
                        # Remove NaN or invalid values
                        valid_mask = np.isfinite(wavelength) & np.isfinite(flux) & (flux != 0)
                        wavelength = wavelength[valid_mask]
                        flux = flux[valid_mask]
                        
                        if len(wavelength) > 0:
                            # Estimate z from Lyman-alpha peak (rest wavelength = 0.1216 microns)
                            lyman_rest = 0.1216
                            peak_idx = np.argmax(flux)
                            lyman_obs = wavelength[peak_idx]
                            z_obs = (lyman_obs / lyman_rest) - 1
                            
                            # Calculate luminosity distance (x)
                            distance = Planck18.luminosity_distance(z_obs)
                            x_mpc = distance.to(u.Mpc).value
                            x_m = distance.to(u.m).value
                            
                            # Calculate tau (delay) with k=0.05
                            c = 3e8  # m/s
                            k = 0.05
                            tau = k * x_m / c
                            delta_z = tau * c / x_m  # Should be ~k due to simplification
                            
                            # Model redshift (adjusted for delay)
                            z_model = z_obs - delta_z
                            
                            # Age in ΛCDM for observed z and model z
                            age_lcdm_obs = Planck18.age(z_obs).value
                            age_model = Planck18.age(z_model).value
                            
                            # Store results
                            results.append({
                                'File': file,
                                'z_observed': z_obs,
                                'z_model': z_model,
                                'delta_z': delta_z,
                                'Distance_Mpc': x_mpc,
                                'Tau_s': tau,
                                'Age_ΛCDM_Gyr': age_lcdm_obs,
                                'Age_Model_Gyr': age_model
                            })
                            
                            print(f"Processed {file}: z_obs={z_obs:.2f}, z_model={z_model:.2f}, delta_z={delta_z:.2f}")
                    else:
                        print(f"File {file}: Missing WAVELENGTH or FLUX columns")
                else:
                    print(f"File {file}: Data is not in expected table format")
            else:
                print(f"File {file}: No EXTRACT1D extension found")

        # Check if it's an s2d file (2D spectral data)
        elif 's2d' in file.lower():
            if len(hdul) > 1 and 'SCI' in hdul[1].name:
                sci_data = hdul[1].data
                wavelength_data = hdul[3].data if len(hdul) > 3 and 'WAVELENGTH' in hdul[3].name else None
                
                if sci_data is not None and wavelength_data is not None:
                    # Extract 1D spectrum by averaging middle row
                    middle_row = sci_data.shape[0] // 2
                    flux_1d = sci_data[middle_row, :]
                    wavelength_1d = wavelength_data[middle_row, :]
                    
                    # Remove NaN or invalid values
                    valid_mask = np.isfinite(wavelength_1d) & np.isfinite(flux_1d) & (flux_1d != 0)
                    wavelength_1d = wavelength_1d[valid_mask]
                    flux_1d = flux_1d[valid_mask]
                    
                    if len(wavelength_1d) > 0:
                        # Estimate z from Lyman-alpha peak
                        lyman_rest = 0.1216
                        peak_idx = np.argmax(flux_1d)
                        lyman_obs = wavelength_1d[peak_idx]
                        z_obs = (lyman_obs / lyman_rest) - 1
                        
                        # Calculate luminosity distance (x)
                        distance = Planck18.luminosity_distance(z_obs)
                        x_mpc = distance.to(u.Mpc).value
                        x_m = distance.to(u.m).value
                        
                        # Calculate tau (delay) with k=0.05
                        c = 3e8
                        k = 0.05
                        tau = k * x_m / c
                        delta_z = tau * c / x_m
                        
                        # Model redshift (adjusted for delay)
                        z_model = z_obs - delta_z
                        
                        # Age in ΛCDM for observed z and model z
                        age_lcdm_obs = Planck18.age(z_obs).value
                        age_model = Planck18.age(z_model).value
                        
                        # Store results
                        results.append({
                            'File': file,
                            'z_observed': z_obs,
                            'z_model': z_model,
                            'delta_z': delta_z,
                            'Distance_Mpc': x_mpc,
                            'Tau_s': tau,
                            'Age_ΛCDM_Gyr': age_lcdm_obs,
                            'Age_Model_Gyr': age_model
                        })
                        
                        print(f"Processed {file}: z_obs={z_obs:.2f}, z_model={z_model:.2f}, delta_z={delta_z:.2f}")
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

print(f"\nSuccessfully processed {len(results)} files out of {len(fits_files)} total files.")

# Step 2: Create charts if results exist
if results:
    # Set up matplotlib for better scientific plots
    plt.style.use('default')
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['lines.linewidth'] = 2
    
    # Chart 1: Age vs z_observed (Scatter)
    plt.figure(figsize=(10, 8))
    plt.scatter([r['z_observed'] for r in results], [r['Age_ΛCDM_Gyr'] for r in results], 
                color='blue', label='ΛCDM Age', alpha=0.7, s=50)
    plt.scatter([r['z_observed'] for r in results], [r['Age_Model_Gyr'] for r in results], 
                color='red', label='Time Delay Model Age', alpha=0.7, s=50)
    plt.xlabel('Observed Redshift (z)', fontsize=14)
    plt.ylabel('Age (Gyr)', fontsize=14)
    plt.title('Age vs Redshift for JADES-GS-z14-0 High-z Galaxies', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/age_vs_z.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 2: Average Age Bar Chart
    avg_age_lcdm = np.mean([r['Age_ΛCDM_Gyr'] for r in results])
    avg_age_model = np.mean([r['Age_Model_Gyr'] for r in results])
    std_age_lcdm = np.std([r['Age_ΛCDM_Gyr'] for r in results])
    std_age_model = np.std([r['Age_Model_Gyr'] for r in results])
    
    plt.figure(figsize=(8, 8))
    bars = plt.bar(['ΛCDM Model', 'Time Delay Model'], [avg_age_lcdm, avg_age_model], 
                   color=['blue', 'red'], alpha=0.7, width=0.6)
    plt.errorbar(['ΛCDM Model', 'Time Delay Model'], [avg_age_lcdm, avg_age_model], 
                 yerr=[std_age_lcdm, std_age_model], fmt='none', color='black', capsize=5, capthick=2)
    plt.xlabel('Cosmological Model', fontsize=14)
    plt.ylabel('Average Age (Gyr)', fontsize=14)
    plt.title('Average Age Comparison: ΛCDM vs Time Delay Model', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars, [avg_age_lcdm, avg_age_model]):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('images/avg_age_bar.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 3: delta_z vs Distance
    plt.figure(figsize=(10, 8))
    distances = [r['Distance_Mpc'] for r in results]
    delta_zs = [r['delta_z'] for r in results]
    plt.scatter(distances, delta_zs, color='green', alpha=0.7, s=50)
    
    # Add trend line
    z = np.polyfit(distances, delta_zs, 1)
    p = np.poly1d(z)
    plt.plot(distances, p(distances), "r--", alpha=0.8, linewidth=2, 
             label=f'Trend line (slope: {z[0]:.2e})')
    
    plt.xlabel('Distance (Mpc)', fontsize=14)
    plt.ylabel('Δz (Redshift Shift)', fontsize=14)
    plt.title('Redshift Shift vs Distance for JADES-GS-z14-0 Galaxies', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/delta_z_vs_distance.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 4: Sample Spectrum (for the first file as an example)
    if results:
        first_file = results[0]['File']
        hdul = fits.open(os.path.join(folder_path, first_file))
        if 'x1d' in first_file.lower() and len(hdul) > 1 and 'EXTRACT1D' in hdul[1].name:
            data = hdul[1].data
            wavelength = data['WAVELENGTH']
            flux = data['FLUX']
            valid_mask = np.isfinite(wavelength) & np.isfinite(flux) & (flux != 0)
            wavelength = wavelength[valid_mask]
            flux = flux[valid_mask]
            plt.figure(figsize=(12, 8))
            plt.plot(wavelength, flux, 'b-', linewidth=1.5, label=f'Spectrum: {first_file}')
            plt.xlabel('Wavelength (μm)', fontsize=14)
            plt.ylabel('Flux', fontsize=14)
            plt.title(f'Sample Spectrum from JADES-GS-z14-0 (z ≈ {results[0]["z_observed"]:.2f})', 
                     fontsize=16, fontweight='bold')
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('images/sample_spectrum.png', dpi=300, bbox_inches='tight')
            plt.close()
        elif 's2d' in first_file.lower() and len(hdul) > 1 and 'SCI' in hdul[1].name:
            sci_data = hdul[1].data
            wavelength_data = hdul[3].data if len(hdul) > 3 and 'WAVELENGTH' in hdul[3].name else None
            if sci_data is not None and wavelength_data is not None:
                middle_row = sci_data.shape[0] // 2
                flux_1d = sci_data[middle_row, :]
                wavelength_1d = wavelength_data[middle_row, :]
                valid_mask = np.isfinite(wavelength_1d) & np.isfinite(flux_1d) & (flux_1d != 0)
                wavelength_1d = wavelength_1d[valid_mask]
                flux_1d = flux_1d[valid_mask]
                plt.figure(figsize=(12, 8))
                plt.plot(wavelength_1d, flux_1d, 'b-', linewidth=1.5, label=f'Spectrum: {first_file}')
                plt.xlabel('Wavelength (μm)', fontsize=14)
                plt.ylabel('Flux', fontsize=14)
                plt.title(f'Sample Spectrum from JADES-GS-z14-0 (z ≈ {results[0]["z_observed"]:.2f})', 
                         fontsize=16, fontweight='bold')
                plt.legend(fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig('images/sample_spectrum.png', dpi=300, bbox_inches='tight')
                plt.close()
        hdul.close()

    # Summary statistics
    print(f"\n📊 Analysis Summary:")
    print(f"   • Total galaxies analyzed: {len(results)}")
    print(f"   • Redshift range: {min([r['z_observed'] for r in results]):.2f} - {max([r['z_observed'] for r in results]):.2f}")
    print(f"   • Average observed redshift: {np.mean([r['z_observed'] for r in results]):.2f}")
    print(f"   • Average model redshift: {np.mean([r['z_model'] for r in results]):.2f}")
    print(f"   • Average Δz: {np.mean([r['delta_z'] for r in results]):.3f}")
    print(f"   • Average ΛCDM age: {avg_age_lcdm:.3f} ± {std_age_lcdm:.3f} Gyr")
    print(f"   • Average model age: {avg_age_model:.3f} ± {std_age_model:.3f} Gyr")
    
    print(f"\n📈 Charts generated in images/ folder:")
    print(f"   • images/age_vs_z.png - Age vs redshift comparison")
    print(f"   • images/avg_age_bar.png - Average age comparison")
    print(f"   • images/delta_z_vs_distance.png - Redshift shift vs distance")
    print(f"   • images/sample_spectrum.png - Sample spectrum visualization")
    
else:
    print("❌ No valid results to create charts.")

