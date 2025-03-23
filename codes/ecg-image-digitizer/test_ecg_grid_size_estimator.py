
import os
import cv2
import matplotlib.pyplot as plt

from ecg_grid_size_from_paper import ecg_grid_size_from_paper
from ecg_gridest_margdist import ecg_gridest_margdist
from ecg_gridest_spectral import ecg_gridest_spectral
from ecg_gridest_matchedfilt import ecg_gridest_matchedfilt

data_path = "./sample-data/ecg-images"  # À adapter selon ton arborescence

for file_name in os.listdir(data_path):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(data_path, file_name)
        img = cv2.imread(image_path)

        print(f"Image : {file_name}")

        # Méthode 1 : estimation papier
        coarse, fine = ecg_grid_size_from_paper(img, paper_width=21.0, unit='cm')
        print(f"  Papier : coarse = {coarse:.2f}px, fine = {fine:.2f}px")

        # Méthode 2 : margdist
        grid_h, grid_v, *_ = ecg_gridest_margdist(img)
        print(f"  Margdist : H = {grid_h}px, V = {grid_v}px")

        # Méthode 3 : spectrale
        grids_hor, grids_ver = ecg_gridest_spectral(img)
        print(f"  Spectral : H = {grids_hor}, V = {grids_ver}")

        # Méthode 4 : matched filter
        grids, powers, best, *_ = ecg_gridest_matchedfilt(img)
        print(f"  MatchedFilt : Best = {best}px, Candidates = {grids}")
        print("-" * 60)
