# ECG Image Kit (version étendue)

Ce dépôt contient des outils avancés pour la digitalisation, l'analyse et la génération de tracés ECG à partir d'images. Il inclut une application Web Streamlit complète pour extraire automatiquement les signaux ECG depuis des photos ou scans papier.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/spripon/ecg-image-kit/main/codes/ecg-image-digitizer/app.py)

---

## Contenu du dépôt

- `codes/ecg-image-digitizer/` :  
  → Contient l’application Streamlit **ECG Image Digitizer** :
  - Détection automatique des dérivations ECG (YOLOv7)
  - Estimation de la grille ECG (4 méthodes)
  - Extraction du signal numérique et export CSV
  - Web app déployable via [streamlit.io](https://streamlit.io)

- `codes/ecg-image-generator/` :  
  → Outils pour générer des images ECG synthétiques

- `sample-data/` :  
  → Exemples d’images ECG papier utilisables pour tester les outils

---

## Lancer localement l'application Streamlit

```bash
cd codes/ecg-image-digitizer
pip install -r requirements.txt
streamlit run app.py
```

---

## Déploiement

- Fork ou clone ce dépôt
- Va sur [streamlit.io/cloud](https://streamlit.io/cloud)
- Crée une nouvelle app avec :
  - Repo : `spripon/ecg-image-kit`
  - Fichier d’entrée : `codes/ecg-image-digitizer/app.py`

---

## Crédits

- Basé sur le projet open-source [alphanumericslab/ecg-image-kit](https://github.com/alphanumericslab/ecg-image-kit)
- YOLOv7 pour la détection automatique de dérivations ECG
- Conversion MATLAB → Python des fonctions de calibration ECG