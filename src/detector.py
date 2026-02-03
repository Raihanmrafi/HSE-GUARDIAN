import cv2
import math
import cvzone
from ultralytics import YOLO

class HSEDetector:
    # PERHATIKAN BARIS INI: Harus ada 'model_path' dan 'conf_threshold'
    def __init__(self, model_path, conf_threshold=0.45):
        
        print(f"🔄 HSEDetector: Loading model from {model_path}...")
        
        # Load Model YOLO
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        self.conf_threshold = conf_threshold
        
        # Definisi Warna (BGR)
        self.COLOR_SAFE = (0, 255, 0)      # Hijau
        self.COLOR_UNSAFE = (0, 0, 255)    # Merah
        self.COLOR_NEUTRAL = (255, 255, 0) # Kuning

    def detect(self, img):
        # 1. Lakukan Prediksi
        results = self.model(img, stream=True, verbose=False)
        
        violations = [] 

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Confidence Check
                conf = math.ceil((box.conf[0] * 100)) / 100
                if conf < self.conf_threshold:
                    continue

                # Koordinat
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                
                # Class Name
                cls = int(box.cls[0])
                current_class = self.class_names[cls]

                # --- LOGIKA SAFETY ---
                color = self.COLOR_NEUTRAL
                label = f"{current_class} {conf}"

                if "NO-" in current_class:
                    color = self.COLOR_UNSAFE
                    label = f"VIOLATION: {current_class}"
                    violations.append(current_class)
                
                elif current_class in ["Hardhat", "Safety Vest", "Mask", "Gloves", "Vest", "Helmet"]:
                    color = self.COLOR_SAFE
                
                # Visualisasi
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=color)
                cvzone.putTextRect(img, label, (max(0, x1), max(35, y1)), 
                                   scale=1, thickness=1, colorR=color, offset=5)

        return img, violations