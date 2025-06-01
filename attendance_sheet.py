import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime, timedelta
import calendar

def create_header_info(class_name, academic_year=None):
    """Création des informations d'en-tête"""
    if academic_year is None:
        current_year = datetime.now().year
        academic_year = f"{current_year}-{current_year + 1}"
    
    return {
        'class_name': class_name,
        'academic_year': academic_year,
        'institution': "École Supérieure de Technologie",
        'department': "Département Informatique"
    }

def generate_session_dates(num_sessions, start_date=None):
    """Génération des dates de séances (hebdomadaires)"""
    if start_date is None:
        start_date = datetime.now()
    
    # Ajuster au prochain lundi si ce n'est pas déjà un lundi
    days_until_monday = (7 - start_date.weekday()) % 7
    if days_until_monday == 0 and start_date.weekday() != 0:
        days_until_monday = 7
    
    first_monday = start_date + timedelta(days=days_until_monday)
    
    sessions = []
    for i in range(num_sessions):
        session_date = first_monday + timedelta(weeks=i)
        sessions.append({
            'date': session_date,
            'formatted': session_date.strftime("%d/%m/%Y"),
            'day_name': calendar.day_name[session_date.weekday()]
        })
    
    return sessions

def create_student_list(num_students, class_name="GI"):
    """Génération d'une liste d'étudiants génériques"""
    students = []
    
    # Prénoms et noms marocains courants
    prenoms = [
        "Ahmed", "Mohamed", "Fatima", "Aicha", "Youssef", "Khadija", "Omar", "Zineb",
        "Hassan", "Salma", "Karim", "Nadia", "Rachid", "Laila", "Abdelaziz", "Amina",
        "Khalid", "Samira", "Mustapha", "Houda", "Jamal", "Rajae", "Samir", "Widad",
        "Abderrahim", "Ghizlane", "Brahim", "Siham", "Hamza", "Ikram"
    ]
    
    noms = [
        "ALAMI", "BENALI", "TAZI", "FASSI", "IDRISSI", "BERRADA", "CHERKAOUI", "BENNANI",
        "HAKIMI", "LAHLOU", "SEFRIOUI", "SABRI", "BENJELLOUN", "KETTANI", "ANDALOUSSI", "FILALI",
        "BENKIRANE", "ZERHOUNI", "AMRANI", "BOUAZZA", "CHERIF", "MAHDI", "OUALI", "SEKKAT",
        "YOUSFI", "HASSANI", "LAMRANI", "QADIRI", "BASRI", "NACIRI"
    ]
    
    for i in range(num_students):
        prenom = prenoms[i % len(prenoms)]
        nom = noms[i % len(noms)]
        
        # Éviter les doublons en ajoutant un numéro si nécessaire
        if i >= len(prenoms) * len(noms):
            nom += f" {i // (len(prenoms) * len(noms)) + 1}"
        
        students.append({
            'numero': i + 1,
            'nom_complet': f"{prenom} {nom}",
            'code_etudiant': f"{class_name}{str(i + 1).zfill(3)}"
        })
    
    return students

def create_attendance_table(students, sessions):
    """Création du tableau de présence"""
    # En-tête du tableau
    header_row = ['N°', 'Nom et Prénom', 'Code Étudiant']
    
    # Ajout des colonnes pour chaque séance
    for session in sessions:
        header_row.append(f"Séance\n{session['formatted']}")
    
    # Ligne des totaux
    header_row.append('Total\nPrésences')
    
    # Données du tableau
    table_data = [header_row]
    
    # Lignes pour chaque étudiant
    for student in students:
        student_row = [
            str(student['numero']),
            student['nom_complet'],
            student['code_etudiant']
        ]
        
        # Cases vides pour chaque séance
        for _ in sessions:
            student_row.append('')
        
        # Case pour le total
        student_row.append('')
        
        table_data.append(student_row)
    
    return table_data

def style_attendance_table(table_data, num_sessions):
    """Application des styles au tableau"""
    table = Table(table_data)
    
    # Calcul des largeurs de colonnes
    col_widths = [1*cm, 5*cm, 2.5*cm]  # N°, Nom, Code
    session_width = (A4[0] - 8.5*cm - 2*cm) / (num_sessions + 1)  # Répartition équitable
    
    for _ in range(num_sessions + 1):  # +1 pour la colonne total
        col_widths.append(session_width)
    
    table._argW = col_widths
    
    # Styles du tableau
    table_style = [
        # Style de l'en-tête
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        
        # Style du contenu
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        
        # Bordures
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.navy),
        
        # Alignement spécifique
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Numéros centrés
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Noms à gauche
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'), # Codes et cases centrés
        
        # Alternance de couleurs pour les lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        
        # Colonne des totaux en surbrillance
        ('BACKGROUND', (-1, 0), (-1, -1), colors.lightyellow),
        ('LINEAFTER', (-2, 0), (-2, -1), 2, colors.navy),
        
        # Hauteur des lignes
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    
    table.setStyle(TableStyle(table_style))
    return table

def create_attendance_pdf_document(class_name, num_sessions, num_students, output_path):
    """Création du document PDF de feuille de présence"""
    try:
        # Configuration du document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.navy
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        header_info_style = ParagraphStyle(
            'HeaderInfo',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=6
        )
        
        # Contenu du document
        story = []
        
        # Informations d'en-tête
        header_info = create_header_info(class_name)
        
        story.append(Paragraph(header_info['institution'], title_style))
        story.append(Paragraph(header_info['department'], subtitle_style))
        story.append(Spacer(1, 20))
        
        # Informations de la classe
        story.append(Paragraph(f"<b>Classe:</b> {header_info['class_name']}", header_info_style))
        story.append(Paragraph(f"<b>Année académique:</b> {header_info['academic_year']}", header_info_style))
        story.append(Paragraph(f"<b>Nombre d'étudiants:</b> {num_students}", header_info_style))
        story.append(Paragraph(f"<b>Nombre de séances:</b> {num_sessions}", header_info_style))
        story.append(Spacer(1, 20))
        
        # Génération des données
        students = create_student_list(num_students, class_name.split('-')[0] if '-' in class_name else class_name)
        sessions = generate_session_dates(num_sessions)
        
        # Tableau de présence
        table_data = create_attendance_table(students, sessions)
        table = style_attendance_table(table_data, num_sessions)
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Instructions
        instructions = [
            "<b>Instructions:</b>",
            "• Marquer 'P' pour Présent, 'A' pour Absent, 'R' pour Retard",
            "• Compléter la colonne 'Total Présences' en fin de semestre",
            "• Conserver ce document pour les évaluations continues"
        ]
        
        for instruction in instructions:
            story.append(Paragraph(instruction, styles['Normal']))
        
        # Construction du PDF
        doc.build(story)
        
        print(f"✅ Feuille de présence créée: {output_path}")
        print(f"📊 {num_students} étudiants, {num_sessions} séances")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Erreur création PDF: {e}")
        return None

def generate_attendance_pdf(class_name, num_sessions, num_students, output_path):
    """Fonction principale de génération de feuille de présence"""
    try:
        # Validation des paramètres
        if num_sessions < 1 or num_sessions > 20:
            raise ValueError("Le nombre de séances doit être entre 1 et 20")
        
        if num_students < 1 or num_students > 100:
            raise ValueError("Le nombre d'étudiants doit être entre 1 et 100")
        
        if not class_name.strip():
            raise ValueError("Le nom de la classe ne peut pas être vide")
        
        # Création du répertoire de sortie
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Génération du PDF
        result_path = create_attendance_pdf_document(class_name, num_sessions, num_students, output_path)
        
        return result_path
        
    except Exception as e:
        print(f"❌ Erreur génération feuille: {e}")
        return None

# Test du module
if __name__ == "__main__":
    test_output = "test_attendance.pdf"
    
    result = generate_attendance_pdf("GI-S5", 6, 30, test_output)
    if result:
        print("Test réussi!")
    else:
        print("Test échoué!")