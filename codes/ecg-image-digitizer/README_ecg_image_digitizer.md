# ECG Image Digitizer (Streamlit App)

Cette application web permet de digitaliser des tracés ECG à partir d'images (photo ou scan papier) en utilisant des outils 100 % Python, intégrés dans une interface Streamlit.

## Fonctionnalités

- Téléversement d'une image ECG
- Estimation automatique de la taille de la grille ECG via 4 méthodes :
  - Basée sur la largeur du papier (méthode papier)
  - Méthode des marges (MargDist)
  - Méthode spectrale (FFT)
  - Méthode par filtre adapté (Matched Filter)
- Extraction du tracé ECG numérique avec différentes méthodes :
  - `center-of-mass`
  - `mean`
  - `max`
- Affichage du tracé et export en CSV

## Structure recommandée

Ce dossier contient :

- `app.py` : Application principale Streamlit
- Fichiers Python de traitement :
  - `ecg_grid_size_from_paper.py`
  - `ecg_gridest_margdist.py`
  - `ecg_gridest_spectral.py`
  - `ecg_gridest_matchedfilt.py`
  - `image_to_sequence.py`
  - `tanh_sat.py`
- `requirements.txt` : dépendances nécessaires pour exécuter l’application

## Lancer l'application localement

```bash
cd codes/ecg-image-digitizer
pip install -r requirements.txt
streamlit run app.py
```

## Déploiement Streamlit Cloud

- Repo : `https://github.com/spripon/ecg-image-kit`
- Fichier d’entrée : `codes/ecg-image-digitizer/app.py`

## À propos

Ce projet est basé sur le dépôt open-source [ecg-image-kit](https://github.com/alphanumericslab/ecg-image-kit), adapté ici pour un usage médical interactif via Streamlit.

Développé avec amour pour la cardiologie numérique.