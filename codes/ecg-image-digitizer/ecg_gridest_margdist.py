
import numpy as np
import cv2
from scipy.signal import find_peaks

def ecg_gridest_margdist(img, distance=10, prominence=0.1):
    """
    Estime la taille de la grille ECG à partir des marges horizontales et verticales.
    
    Paramètres :
    - img : image ECG (2D ou 3D)
    - distance : distance minimale entre pics pour la détection
    - prominence : proéminence minimale pour les pics

    Retourne :
    - grid_size_hor : taille de la grille horizontale (en pixels)
    - grid_size_ver : taille de la grille verticale (en pixels)
    - gaps_hor : distances entre pics horizontaux
    - gaps_ver : distances entre pics verticaux
    - peaks_hor : positions des pics horizontaux
    - peaks_ver : positions des pics verticaux
    """

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = img.astype(np.float32)

    marg_hor = np.sum(img, axis=0)  # Marginale horizontale (colonnes)
    marg_ver = np.sum(img, axis=1)  # Marginale verticale (lignes)

    peaks_hor, _ = find_peaks(marg_hor, distance=distance, prominence=prominence*np.max(marg_hor))
    peaks_ver, _ = find_peaks(marg_ver, distance=distance, prominence=prominence*np.max(marg_ver))

    gaps_hor = np.diff(peaks_hor)
    gaps_ver = np.diff(peaks_ver)

    grid_size_hor = np.median(gaps_hor) if len(gaps_hor) > 0 else None
    grid_size_ver = np.median(gaps_ver) if len(gaps_ver) > 0 else None

    return grid_size_hor, grid_size_ver, gaps_hor, gaps_ver, peaks_hor, peaks_ver
