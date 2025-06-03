from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
import os

def insert_image_into_excel(image_path, output_excel_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Image Scannée"

    # Charger l'image (doit être PNG ou JPEG)
    img = XLImage(image_path)

    # Ajuster la taille de l'image si nécessaire (facultatif)
    img.width = img.width * 0.5
    img.height = img.height * 0.5

    # Insérer dans la cellule A1
    ws.add_image(img, 'A1')

    # Sauvegarder
    wb.save(output_excel_path)
    print(f"✅ Image insérée dans {output_excel_path}")
