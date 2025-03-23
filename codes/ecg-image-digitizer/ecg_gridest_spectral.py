
import numpy as np
import cv2
from scipy.signal import find_peaks

def ecg_gridest_spectral(img, patch_size=128, prominence=0.1):
    """
    Estime la taille de la grille ECG à partir d'une analyse spectrale (FFT 2D).

    Paramètres :
    - img : image ECG (2D ou 3D)
    - patch_size : taille des sous-images pour FFT
    - prominence : seuil pour détecter les pics spectraux

    Retourne :
    - grid_sizes_hor : tailles estimées de grille horizontale (en pixels)
    - grid_sizes_ver : tailles estimées de grille verticale (en pixels)
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = img.astype(np.float32)
    h, w = img.shape
    n_patches_x = w // patch_size
    n_patches_y = h // patch_size

    avg_spectrum = np.zeros((patch_size, patch_size))

    for i in range(n_patches_y):
        for j in range(n_patches_x):
            patch = img[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size]
            f = np.fft.fft2(patch)
            fshift = np.fft.fftshift(f)
            magnitude = np.abs(fshift)
            avg_spectrum += magnitude

    avg_spectrum /= (n_patches_x * n_patches_y)

    # Profils spectraux horizontaux et verticaux
    spectrum_hor = np.sum(avg_spectrum, axis=0)
    spectrum_ver = np.sum(avg_spectrum, axis=1)

    peaks_hor, _ = find_peaks(spectrum_hor, prominence=prominence * np.max(spectrum_hor))
    peaks_ver, _ = find_peaks(spectrum_ver, prominence=prominence * np.max(spectrum_ver))

    # Convertir fréquence en période (en pixels)
    def freqs_to_periods(peaks, N):
        freqs = np.fft.fftfreq(N)
        freqs = np.fft.fftshift(freqs)
        positive_freqs = freqs[peaks]
        periods = np.abs(1 / positive_freqs[positive_freqs != 0])
        return np.sort(periods)

    grid_sizes_hor = freqs_to_periods(peaks_hor, patch_size)
    grid_sizes_ver = freqs_to_periods(peaks_ver, patch_size)

    return grid_sizes_hor, grid_sizes_ver
