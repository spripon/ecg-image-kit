
def ecg_grid_size_from_paper(image, paper_width, unit='cm'):
    """
    Estime la taille de la grille ECG (grille large et fine) en pixels.

    Paramètres :
    - image : image ECG chargée via OpenCV (2D ou 3D)
    - paper_width : largeur physique du papier (par exemple 21 cm)
    - unit : 'cm' ou 'in'

    Retourne :
    - coarse_grid_res : taille de la grille large en pixels (5 mm)
    - fine_grid_res : taille de la grille fine en pixels (1 mm)
    """
    import cv2

    # Largeur de l’image en pixels
    img_width_px = image.shape[1]

    # Conversion de l’unité en pouces
    if unit == 'cm':
        paper_width_in = paper_width / 2.54
    elif unit == 'in':
        paper_width_in = paper_width
    else:
        raise ValueError("Unité non reconnue : choisir 'cm' ou 'in'")

    # Calcul du DPI de l’image
    dpi = img_width_px / paper_width_in

    # 5 mm = 0.19685 inch (grille large)
    # 1 mm = 0.03937 inch (grille fine)
    coarse_grid_res = dpi * 0.19685
    fine_grid_res = dpi * 0.03937

    return coarse_grid_res, fine_grid_res
