# Redéploiement pour forcer Streamlit Cloud à lire packages.txt

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
from image_to_sequence import image_to_sequence
from detect_leads import detect_roi_yolov7

st.set_page_config(layout="wide")
st.title("ECG Image Digitizer - Streamlit App (YOLOv7 + Grid Estimation + Signal Extraction)")

uploaded_file = st.file_uploader("Télécharger une image ECG (photo ou scan)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    img_path = tfile.name

    st.image(img_path, caption="Image ECG originale", use_column_width=True)

    st.subheader("1. Détection automatique des dérivations ECG avec YOLOv7")

    try:
        results_dir = detect_roi_yolov7(img_path)
        roi_images = []
        for fname in os.listdir(results_dir):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                roi_images.append(os.path.join(results_dir, fname))

        if not roi_images:
            st.error("Aucune dérivation ECG détectée.")
        else:
            st.success(f"{len(roi_images)} dérivation(s) détectée(s).")
            for idx, roi_path in enumerate(roi_images):
                st.image(roi_path, caption=f"Dérivation {idx + 1}", width=300)

            st.subheader("2. Extraction du signal ECG à partir des ROI")

            method = st.selectbox("Méthode d'extraction :", ['center-of-mass', 'mean', 'max'])
            for idx, roi_path in enumerate(roi_images):
                roi_img = cv2.imread(roi_path)
                signal = image_to_sequence(roi_img, mode='dark', method=method)

                st.markdown(f"**Dérivation {idx + 1}**")
                st.line_chart(signal)

                csv_data = '\n'.join(map(str, signal))
                st.download_button(
                    label=f"Télécharger dérivation {idx + 1} (CSV)",
                    data=csv_data,
                    file_name=f"ecg_derivation_{idx + 1}.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"Erreur lors de la détection YOLOv7 : {e}")

    st.subheader("3. Estimation de la grille ECG")

    img = cv2.imread(img_path)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Méthode papier (21 cm)**")
        coarse, fine = ecg_grid_size_from_paper(img, 21.0, 'cm')
        st.write(f"Taille grille large : {coarse:.2f} px")
        st.write(f"Taille grille fine : {fine:.2f} px")

    with col2:
        st.markdown("**Méthode margdist**")
        grid_h, grid_v, *_ = ecg_gridest_margdist(img)
        st.write(f"Horizontale : {grid_h} px")
        st.write(f"Verticale : {grid_v} px")

    st.markdown("**Méthode spectrale**")
    grids_hor, grids_ver = ecg_gridest_spectral(img)
    st.write(f"Grilles horizontales candidates : {np.round(grids_hor, 2)}")
    st.write(f"Grilles verticales candidates : {np.round(grids_ver, 2)}")

    st.markdown("**Méthode matched filter**")
    grids, powers, best, *_ = ecg_gridest_matchedfilt(img)
    st.write(f"Meilleure taille détectée : {best}px")
    st.line_chart(powers)