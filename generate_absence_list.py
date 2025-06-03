import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

def generate_absence_list(filiere="GINF2", num_seances=6, output_format="excel"):
    """
    Génère une liste d'absence selon les paramètres spécifiés
    
    Args:
        filiere (str): La filière (GINF1, GINF2, GINF3)
        num_seances (int): Nombre de séances à inclure
        output_format (str): 'excel' ou 'pdf' - format de sortie
        
    Returns:
        str: Chemin du fichier généré
    """
    # Créer le dossier si nécessaire
    os.makedirs("generated_files", exist_ok=True)
    
    # Générer le nom de fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Liste_Absence_{filiere}_{num_seances}seances_{timestamp}"
    
    if output_format == "excel":
        return generate_excel_absence_list(filiere, num_seances, filename)
    else:
        return generate_pdf_absence_list(filiere, num_seances, filename)

def generate_excel_absence_list(filiere, num_seances, filename):
    """Ajoute des colonnes de séances à un fichier existant"""
    input_path = os.path.join("inputs", "Liste_abssence.xlsx")
    output_path = os.path.join("generated_files", f"{filename}.xlsx")
    
    # Lire le fichier existant
    df = pd.read_excel(input_path)
    
    # Ajouter les colonnes de séances
    for i in range(1, num_seances + 1):
        df[f"Séance {i}"] = ""
    
    # Sauvegarder avec mise en forme
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=f"Absences {filiere}")
        
        workbook = writer.book
        worksheet = writer.sheets[f"Absences {filiere}"]
        
        # Mise en forme de l'en-tête
        header_fmt = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_fmt)
            worksheet.set_column(col_num, col_num, 15)  # Ajuste largeur colonne

    return output_path


def generate_pdf_absence_list(filiere, num_seances, filename):
    """Génère un fichier PDF de liste d'absence à partir du fichier Excel modifié"""
    # D'abord générer l'excel enrichi
    excel_path = generate_excel_absence_list(filiere, num_seances, filename)
    
    # Charger le fichier Excel
    df = pd.read_excel(excel_path)
    
    # Préparer le PDF
    pdf_path = os.path.join("generated_files", f"{filename}.pdf")
    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Titre
    pdf.cell(0, 10, f"Liste d'absence - {filiere} - {num_seances} séances", ln=1, align='C')
    pdf.ln(10)
    
    # Largeur dynamique des colonnes
    col_widths = []
    total_columns = len(df.columns)
    page_width = 280  # largeur approximative d'une page A4 paysage (en mm)
    col_width = page_width / total_columns
    col_widths = [col_width] * total_columns

    # En-têtes
    pdf.set_font("Arial", 'B', 10)
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 10, str(col), border=1, align='C')
    pdf.ln()
    
    # Contenu
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        for i, col in enumerate(df.columns):
            cell_value = str(row[col]) if pd.notna(row[col]) else ""
            pdf.cell(col_widths[i], 10, cell_value, border=1, align='C')
        pdf.ln()
    
    pdf.output(pdf_path)
    return pdf_path

def generate_absence_from_binomes(filiere="GINF2", output_format="excel"):
    """
    Génère une liste d'absence à partir du fichier de binômes existant.
    
    Args:
        filiere (str): Nom de la filière (par défaut GINF2)
        output_format (str): 'excel' ou 'pdf'
    
    Returns:
        str: Chemin du fichier généré
    """
    # Charger le fichier de binômes
    input_path = f"inputs/binomes_{filiere}.xlsx"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Fichier introuvable : {input_path}")
    
    df_binomes = pd.read_excel(input_path)

    # Nettoyer / uniformiser les colonnes si nécessaire
    df_binomes.columns = [c.strip() for c in df_binomes.columns]
    nom_col = df_binomes.columns[0]
    
    # Ajouter colonnes nécessaires
    df_absence = pd.DataFrame()
    df_absence["N°"] = range(1, len(df_binomes) + 1)
    df_absence["Nom et Prénom"] = df_binomes[nom_col]
    df_absence["Groupe"] = ""  # vide par défaut
    for i in range(1, 7):  # 6 séances par défaut
        df_absence[f"Séance {i}"] = ""
    
    # Créer le dossier
    os.makedirs("generated_files", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Absence_Binomes_{filiere}_{timestamp}"
    output_path = os.path.join("generated_files", f"{filename}.{ 'xlsx' if output_format=='excel' else 'pdf' }")
    
    if output_format == "excel":
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df_absence.to_excel(writer, index=False, sheet_name=f"Binômes {filiere}")
            workbook = writer.book
            worksheet = writer.sheets[f"Binômes {filiere}"]
            header_fmt = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            for col_num, value in enumerate(df_absence.columns.values):
                worksheet.write(0, col_num, value, header_fmt)
                worksheet.set_column(col_num, col_num, 18)
    else:
        # Générer le PDF
        from fpdf import FPDF

        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Liste d'absence - Binômes {filiere}", ln=1, align='C')
        pdf.ln(10)

        # Largeurs
        total_columns = len(df_absence.columns)
        col_width = 280 / total_columns
        pdf.set_font("Arial", 'B', 10)
        for col in df_absence.columns:
            pdf.cell(col_width, 10, str(col), border=1, align='C')
        pdf.ln()
        
        # Contenu
        pdf.set_font("Arial", size=10)
        for idx, row in df_absence.iterrows():
            for val in row:
                pdf.cell(col_width, 10, str(val) if pd.notna(val) else "", border=1, align='C')
            pdf.ln()

        pdf.output(output_path)
    
    return output_path

