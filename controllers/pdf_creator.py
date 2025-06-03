import os
import cv2
import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

# Configuration OCR
ocr_engines = {
    "Rapide": PaddleOCR(use_angle_cls=False, lang='fr'),
    "Standard": PaddleOCR(use_angle_cls=True, lang='fr'),
    "Précis": PaddleOCR(use_angle_cls=True, lang='fr',det_db_thresh=0.3)
}

def preprocess_image(image_path):
    """Préprocessing de l'image pour améliorer l'OCR"""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Amélioration du contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Débruitage
    denoised = cv2.fastNlMeansDenoising(enhanced)
    
    # Sauvegarde temporaire de l'image préprocessée
    temp_path = image_path.replace('.', '_processed.')
    cv2.imwrite(temp_path, denoised)
    
    return temp_path, image.shape

def extract_text_with_positions(image_path, quality="Standard"):
    """Extraction du texte avec positions via OCR"""
    try:
        # Préprocessing
        processed_path, original_shape = preprocess_image(image_path)
        
        # Sélection de l'engine OCR
        ocr = ocr_engines.get(quality, ocr_engines["Standard"])
        
        # OCR
        results = ocr.ocr(processed_path)
        
        # Nettoyage du fichier temporaire
        if os.path.exists(processed_path):
            os.remove(processed_path)
        
        text_elements = []
        
        if results and results[0]:
            for line in results[0]:
                try:
                    if len(line) >= 2:
                        bbox = line[0]  # Coordonnées du rectangle
                        text_info = line[1]  # (texte, confiance)
                        
                        if len(text_info) >= 2:
                            text = text_info[0].strip()
                            confidence = text_info[1]
                            
                            if text and confidence > 0.5:  # Filtrer par confiance
                                # Calculer position et taille
                                x_coords = [point[0] for point in bbox]
                                y_coords = [point[1] for point in bbox]
                                
                                x = min(x_coords)
                                y = min(y_coords)
                                width = max(x_coords) - min(x_coords)
                                height = max(y_coords) - min(y_coords)
                                
                                # Estimation de la taille de police
                                font_size = max(8, min(16, height * 0.8))
                                
                                text_elements.append({
                                    'text': text,
                                    'x': x,
                                    'y': y,
                                    'width': width,
                                    'height': height,
                                    'font_size': font_size,
                                    'confidence': confidence
                                })
                                
                except Exception as e:
                    print(f"Erreur lors du traitement d'une ligne OCR: {e}")
                    continue
        
        return text_elements, original_shape
        
    except Exception as e:
        print(f"Erreur OCR: {e}")
        return [], None

def create_searchable_pdf(image_path, output_path, quality="Standard", add_background=True):
    """Créer un PDF avec texte recherchable à partir d'une image"""
    try:
        # Vérification de l'image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image non trouvée: {image_path}")
        
        # Extraction du texte
        text_elements, shape = extract_text_with_positions(image_path, quality)
        
        if shape is None:
            raise ValueError("Impossible de déterminer les dimensions de l'image")
        
        height, width = shape[:2]
        
        # Création du PDF
        doc = fitz.open()
        page = doc.new_page(width=width, height=height)
        
        # Ajout de l'image de fond si demandé
        if add_background:
            rect = fitz.Rect(0, 0, width, height)
            page.insert_image(rect, filename=image_path)
        
        # Ajout du texte invisible/transparent pour la recherche
        text_count = 0
        for element in text_elements:
            try:
                # Position ajustée (PyMuPDF utilise un système de coordonnées différent)
                x = element['x']
                y = element['y'] + element['height']  # Ajustement pour l'origine
                
                # Texte transparent ou semi-transparent
                color = (0, 0, 0) if not add_background else (0.95, 0.95, 0.95)
                
                page.insert_text(
                    (x, y),
                    element['text'],
                    fontsize=element['font_size'],
                    fontname="helv",
                    color=color,
                    overlay=True
                )
                text_count += 1
                
            except Exception as e:
                print(f"Erreur lors de l'insertion du texte '{element['text']}': {e}")
                continue
        
        # Sauvegarde
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        doc.close()
        
        print(f"✅ PDF créé avec succès: {output_path}")
        print(f"📊 Éléments de texte ajoutés: {text_count}")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF: {e}")
        return None

def enhance_image_quality(image_path):
    """Amélioration de la qualité d'image pour OCR"""
    try:
        image = cv2.imread(image_path)
        
        # Redimensionnement si l'image est trop petite
        height, width = image.shape[:2]
        if width < 1000:
            scale = 1000 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Amélioration de la netteté
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Sauvegarde
        enhanced_path = image_path.replace('.', '_enhanced.')
        cv2.imwrite(enhanced_path, sharpened)
        
        return enhanced_path
        
    except Exception as e:
        print(f"Erreur lors de l'amélioration: {e}")
        return image_path

# Test du module
if __name__ == "__main__":
    test_image = "test_image.jpg"
    test_output = "test_output.pdf"
    
    if os.path.exists(test_image):
        result = create_searchable_pdf(test_image, test_output)
        if result:
            print("Test réussi!")
        else:
            print("Test échoué!")
    else:
        print("Image de test non trouvée")