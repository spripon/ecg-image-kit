
import numpy as np
import cv2
from scipy.ndimage import uniform_filter1d

def image_to_sequence(img, mode='dark', method='center-of-mass', windowlen=None, plot_result=False):
    """
    Extrait un signal 1D (série temporelle) depuis une image ECG 2D.

    Paramètres :
    - img : image 2D (ECG ROI), en niveaux de gris
    - mode : 'dark' si le tracé est foncé sur fond clair, 'bright' sinon
    - method : 'max', 'mean', ou 'center-of-mass'
    - windowlen : longueur de lissage facultatif
    - plot_result : pour affichage (non utilisé ici)

    Retour :
    - data : vecteur 1D représentant le signal ECG
    """

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = img.astype(np.float32)

    if mode == 'bright':
        img = 255 - img

    h, w = img.shape
    data = np.zeros(w)

    for x in range(w):
        column = img[:, x]

        if method == 'max':
            y = np.argmax(column)
        elif method == 'mean':
            y = np.mean(np.where(column > np.mean(column))[0])
        elif method == 'center-of-mass':
            weights = column
            positions = np.arange(h)
            if np.sum(weights) == 0:
                y = h / 2
            else:
                y = np.sum(weights * positions) / np.sum(weights)
        else:
            raise ValueError("Méthode inconnue")

        data[x] = y

    # Lissage optionnel
    if windowlen:
        data = uniform_filter1d(data, size=windowlen)

    return data
