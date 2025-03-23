import os
import sys
import subprocess
import uuid

# Ajouter le chemin vers le dossier YOLOv7 pour les imports
yolov7_path = os.path.join(os.path.dirname(__file__), "roi", "yolov7")
sys.path.append(yolov7_path)

def detect_roi_yolov7(image_path, output_dir="roi_output", weights=None, conf=0.25):
    if weights is None:
        weights = os.path.join(os.path.dirname(__file__), "roi", "yolov7", "yolov7_custom.pt")

    output_dir = os.path.join(os.path.dirname(__file__), output_dir, str(uuid.uuid4()))
    os.makedirs(output_dir, exist_ok=True)

    # S'assurer que le fichier a une extension correcte pour YOLOv7
    if not os.path.splitext(image_path)[1]:
        new_path = image_path + ".jpg"
        os.rename(image_path, new_path)
        image_path = new_path

    command = [
        sys.executable, os.path.join(yolov7_path, "detect.py"),
        "--weights", weights,
        "--conf", str(conf),
        "--img-size", "640",
        "--source", image_path,
        "--project", output_dir,
        "--name", "results",
        "--exist-ok"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Erreur YOLOv7 :\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

    result_path = os.path.join(output_dir, "results")
    return result_path
