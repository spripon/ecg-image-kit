import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt

from ecg_grid_size_from_paper import ecg_grid_size_from_paper
from ecg_gridest_margdist import ecg_gridest_margdist
from ecg_gridest_spectral import ecg_gridest_spectral
from ecg_gridest_matchedfilt import ecg_gridest_matchedfilt
from detect_leads import detect_roi_yolov7

st.title("Digitisation ECG avec détection YOLOv7")

uploaded_file = st.file_uploader("Choisissez une image ECG", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.read())
        img_path = tmp_file.name

    # Assurer une extension explicite pour OpenCV
    if not os.path.splitext(img_path)[1]:
        new_img_path = img_path + ".jpg"
        os.rename(img_path, new_img_path)
        img_path = new_img_path

    img = cv2.imread(img_path)

    if img is None:
        st.error("Erreur lors du chargement de l'image.")
    else:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Image ECG originale", use_container_width=True)

        # Détection des dérivations ECG avec YOLOv7
        try:
            roi_path = detect_roi_yolov7(img_path)
            st.success(f"Dérivations détectées sauvegardées dans : {roi_path}")
        except Exception as e:
            st.error(f"Erreur lors de la détection YOLOv7 : {e}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("**Méthode papier (21 cm)**")
            coarse, fine = ecg_grid_size_from_paper(img, 21.0, 'cm')
            st.write(f"Taille grille large : {coarse:.2f} px")
            st.write(f"Taille grille fine : {fine:.2f} px")

        with col2:
            st.markdown("**Méthode Margdist**")
            result_margdist = ecg_gridest_margdist(img)
            st.write(f"Résultat : {result_margdist[0]:.2f} px" if isinstance(result_margdist, tuple) else f"Résultat : {result_margdist:.2f} px")

        with col3:
            st.markdown("**Méthode Spectrale**")
            result_spectral = ecg_gridest_spectral(img)
            st.write(f"Résultat : {result_spectral[0]:.2f} px" if isinstance(result_spectral, tuple) else f"Résultat : {result_spectral:.2f} px")

        with col4:
            st.markdown("**Méthode Matched Filter**")
            result_matchedfilt = ecg_gridest_matchedfilt(img)
            st.write(f"Résultat : {result_matchedfilt[0]:.2f} px" if isinstance(result_matchedfilt, tuple) else f"Résultat : {result_matchedfilt:.2f} px")

        # Option téléchargement CSV à compléter
        st.markdown("---")
        st.markdown("### Téléchargement du CSV (fonctionnalité à venir)")
