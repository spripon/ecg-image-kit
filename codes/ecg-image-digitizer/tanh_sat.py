
import numpy as np

def tanh_sat(x, param, mode='ksigma'):
    """
    Applique une saturation douce avec tanh à un signal.

    Paramètres :
    - x : array (1D ou 2D), signal(s) à traiter
    - param : facteur de saturation (k * sigma ou seuil absolu)
    - mode : 'ksigma' (par défaut) ou 'absolute'

    Retour :
    - y : signal saturé
    """
    x = np.asarray(x)
    x_shape = x.shape

    if x.ndim == 1:
        x = x.reshape(1, -1)

    if mode == 'ksigma':
        alpha = param * np.std(x, axis=1, keepdims=True)
    elif mode == 'absolute':
        if np.isscalar(param):
            alpha = np.full((x.shape[0], 1), param)
        elif isinstance(param, (list, np.ndarray)) and len(param) == x.shape[0]:
            alpha = np.array(param).reshape(-1, 1)
        else:
            raise ValueError("param doit être un scalaire ou un vecteur de même taille que le nombre de lignes de x")
    else:
        raise ValueError("mode doit être 'ksigma' ou 'absolute'")

    y = alpha * np.tanh(x / alpha)

    return y.squeeze() if x_shape[0] == 1 else y
