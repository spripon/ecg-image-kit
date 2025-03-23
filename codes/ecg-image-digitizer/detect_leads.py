
import os
import sys
import subprocess
import uuid

# Ajouter le chemin vers le dossier YOLOv7 pour les imports
yolov7_path = os.path.join(os.path.dirname(__file__), "roi", "yolov7")
sys.path.append(yolov7_path)

def detect_roi_yolov7(image_path, output_dir="roi_output", weights="roi/yolov7/yolov7_custom.pt", conf=0.25):
    """
    Lance la détection des ROI ECG à l'aide de YOLOv7 et retourne le chemin du dossier avec les résultats.

    Paramètres :
    - image_path : chemin de l'image ECG
    - output_dir : dossier temporaire pour enregistrer les résultats
    - weights : chemin vers le modèle YOLOv7 entraîné
    - conf : seuil de confiance (par défaut 0.25)

    Retour :
    - output_dir : dossier contenant les ROI détectées (images découpées)
    """
    output_dir = os.path.join(os.path.dirname(__file__), output_dir, str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", os.path.join(yolov7_path, "detect.py"),
        "--weights", weights,
        "--conf", str(conf),
        "--img-size", "640",
        "--source", image_path,
        "--project", output_dir,
        "--name", "results",
        "--exist-ok"
    ]

    subprocess.run(command, check=True)
    result_path = os.path.join(output_dir, "results")
    return result_path
