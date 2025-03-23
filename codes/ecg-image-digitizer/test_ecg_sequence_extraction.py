
import os
import cv2
import matplotlib.pyplot as plt
from image_to_sequence import image_to_sequence

data_path = "./sample-data/ecg-segments"  # À adapter selon ton dossier de segments ECG

methods = ['max', 'mean', 'center-of-mass']

for file_name in os.listdir(data_path):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(data_path, file_name)
        img = cv2.imread(img_path)

        print(f"Image : {file_name}")
        plt.figure(figsize=(10, 4))
        for method in methods:
            signal = image_to_sequence(img, mode='dark', method=method)
            plt.plot(signal, label=method)

        plt.title(f"ECG Extraction - {file_name}")
        plt.legend()
        plt.xlabel("Temps (pixels)")
        plt.ylabel("Position verticale")
        plt.tight_layout()
        plt.show()
