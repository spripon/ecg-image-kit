
import numpy as np
import cv2
from scipy.signal import convolve2d, find_peaks

def create_matched_filter(size):
    """Crée un filtre carré creux (bord blanc, centre noir)"""
    filt = -np.ones((size, size), dtype=np.float32)
    border = max(1, size // 10)
    filt[border:-border, border:-border] = 1
    return filt

def ecg_gridest_matchedfilt(img, min_size=8, max_size=40, step=1, patch_size=128):
    """
    Estime la taille de la grille ECG à l'aide d'un filtrage par gabarit (matched filter).

    Paramètres :
    - img : image ECG (2D ou 3D)
    - min_size, max_size : tailles de filtres testées
    - step : pas d'incrément entre tailles
    - patch_size : taille des segments analysés

    Retourne :
    - grid_sizes : tailles de grille candidates (en pixels)
    - powers : puissances moyennes pour chaque taille
    - best_size : taille avec la plus grande puissance
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = img.astype(np.float32)
    h, w = img.shape

    n_patches_x = w // patch_size
    n_patches_y = h // patch_size

    matched_filter_powers = []

    sizes = list(range(min_size, max_size + 1, step))

    for filt_size in sizes:
        filt = create_matched_filter(filt_size)
        power_sum = 0

        for i in range(n_patches_y):
            for j in range(n_patches_x):
                patch = img[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size]
                response = convolve2d(patch, filt, mode='valid')
                power = np.mean(response ** 2)
                power_sum += power

        avg_power = power_sum / (n_patches_x * n_patches_y)
        matched_filter_powers.append(avg_power)

    matched_filter_powers = np.array(matched_filter_powers)
    peaks, _ = find_peaks(matched_filter_powers)

    grid_sizes = np.array(sizes)[peaks]
    powers = matched_filter_powers[peaks]
    best_size = sizes[np.argmax(matched_filter_powers)]

    return grid_sizes, powers, best_size, matched_filter_powers, sizes
