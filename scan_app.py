import streamlit as st
import os
import tempfile
from PIL import Image
import base64

# Import des modules de traitement
from pdf_creator import create_searchable_pdf
from image_to_excel_converter_local import image_to_excel_converter_local as image_to_excel_converter
from attendance_sheet import generate_attendance_pdf
from group_maker import create_student_groups

# Configuration
st.set_page_config(
    page_title="Smart Scanner System - ENSAT", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Créer les dossiers nécessaires
for folder in ["temp_uploads", "generated_files", "assets"]:
    os.makedirs(folder, exist_ok=True)

# CSS professionnel ENSAT/UAE
st.markdown("""
<style>
    /* Variables CSS - Couleurs officielles ENSAT/UAE */
    /* Variables CSS - Palette de couleurs ENSAT/UAE Premium */
:root {
    --primary-blue: #0f172a;
    --secondary-blue: #1e40af;
    --accent-blue: #3b82f6;
    --light-blue: #60a5fa;
    --primary-orange: #ea580c;
    --secondary-orange: #f97316;
    --accent-orange: #fb923c;
    --success-green: #059669;
    --warning-yellow: #d97706;
    --error-red: #dc2626;
    
    --text-primary: #0f172a;
    --text-secondary: #334155; /* Augmentation du contraste */
    --text-muted: #64748b;
    --text-white: #ffffff;
    
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --bg-tertiary: #e2e8f0;
    --bg-dark: #0f172a;
    
    --border-light: #e2e8f0;
    --border-medium: #cbd5e1;
    --border-dark: #475569;
    
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    
    --transition-fast: all 0.15s ease-in-out;
    --transition-normal: all 0.3s ease-in-out;
    --transition-slow: all 0.5s ease-in-out;
}

/* ================= HEADER REDESIGN ================= */
.institutional-header {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 40%, var(--primary-orange) 100%);
    padding: 2.5rem 2rem;
    border-radius: var(--radius-xl);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-xl);
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 2;
}

/* Logo containers - Taille augmentée */
.logo-container {
    
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    backdrop-filter: blur(10px);
    
    transition: var(--transition-normal);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    width: 150px;
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Images des logos - Taille augmentée */
.logo-container img {
    max-width: 150%;
    max-height: 150%;
    filter: brightness(1.1) contrast(1.1);
    
}

/* Positionnement spécifique des logos */
.header-logos {
    display: flex;
    justify-content: space-between;
    width: 200%;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 0;
    right: 0;
    padding: 0 2rem;
    z-index: 1;
}

/* Texte centré au-dessus des logos */
.header-text {
    text-align: center;
    color: var(--text-white);
    position: relative;
    z-index: 3;
    width: 100%;
    padding: 0 200px; /* Espace pour les logos */
}

.header-text h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 50%, #e2e8f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.header-text p {
    font-size: 1.4rem;
    opacity: 0.95;
    margin: 0 0 1rem 0;
    font-weight: 500;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* ================= TEXT CONTRAST IMPROVEMENTS ================= */
body, .stMarkdown, .stText, .stSelectbox label, .stRadio label, .stCheckbox label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.professional-card h3 {
    color: var(--primary-blue);
    font-size: 1.6rem !important; /* Taille augmentée */
    font-weight: 700 !important;
}

.metric-title {
    font-size: 1.4rem !important; /* Taille augmentée */
}

.metric-description {
    font-size: 1.1rem !important; /* Taille augmentée */
    color: var(--text-secondary) !important;
}

/* ================= TAB REDESIGN ================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--bg-primary);
    padding: 0.5rem;
    border-radius: var(--radius-xl);
    border: 2px solid var(--border-light);
    box-shadow: var(--shadow-lg);
    margin-bottom: 2rem;
}

.stTabs [data-baseweb="tab"] {
    height: 60px;
    padding: 0 2rem;
    font-size: 1.2rem !important; /* Taille augmentée */
    font-weight: 600 !important;
}

/* ================= CARD CONTENT VISIBILITY ================= */
.professional-card {
    background: var(--bg-primary);
    padding: 2rem;
    border-radius: var(--radius-xl);
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-lg);
    margin-bottom: 2rem;
    transition: var(--transition-normal);
}

.professional-card ul li {
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
    line-height: 1.6;
}

/* ================= UPLOAD ZONE ================= */
.upload-zone-modern {
    padding: 3rem 2rem;
}

/* ================= RESPONSIVE ADJUSTMENTS ================= */
@media (max-width: 1024px) {
    .header-text h1 {
        font-size: 2.2rem;
    }
    
    .header-text p {
        font-size: 1.2rem;
    }
    
    .logo-container {
        width: 120px;
        height: 120px;
        padding: 1rem;
    }
}

@media (max-width: 768px) {
    .header-logos {
        position: relative;
        transform: none;
        top: auto;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .header-text {
        padding: 0;
    }
    
    .header-text h1 {
        font-size: 1.8rem;
    }
    
    .logo-container {
        width: 100px;
        height: 100px;
        position: relative;
    }
}

.logo-container:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.logo-container img {
    height: 65px;
    width: auto;
    filter: brightness(1.1) contrast(1.1);
    border-radius: var(--radius-sm);
}

.header-text {
    text-align: center;
    color: var(--text-white);
}

.header-text h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 50%, #e2e8f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.header-text p {
    font-size: 1.25rem;
    opacity: 0.95;
    margin: 0 0 1rem 0;
    font-weight: 500;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.institution-badge {
    background: rgba(255, 255, 255, 0.2);
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-white);
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Navigation Tabs - Redesign complet */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--bg-primary);
    padding: 0.5rem;
    border-radius: var(--radius-xl);
    border: 2px solid var(--border-light);
    box-shadow: var(--shadow-lg);
    margin-bottom: 3rem;
    backdrop-filter: blur(10px);
}

.stTabs [data-baseweb="tab"] {
    height: 70px;
    padding: 0 2rem;
    background: transparent;
    border-radius: var(--radius-lg);
    border: none;
    transition: var(--transition-normal);
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-secondary);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stTabs [data-baseweb="tab"]::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--primary-orange) 100%);
    border-radius: var(--radius-lg);
    transition: var(--transition-normal);
    transform: translate(-50%, -50%);
    z-index: -1;
}

.stTabs [aria-selected="true"] {
    color: var(--text-white);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stTabs [aria-selected="true"]::before {
    width: 100%;
    height: 100%;
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: var(--bg-secondary);
    color: var(--accent-blue);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Cards professionnelles */
.professional-card {
    background: var(--bg-primary);
    padding: 2.5rem;
    border-radius: var(--radius-xl);
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-lg);
    margin-bottom: 2rem;
    transition: var(--transition-normal);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.professional-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, var(--accent-blue) 0%, var(--primary-orange) 100%);
}

.professional-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 200%;
    background: conic-gradient(from 45deg, transparent, rgba(59, 130, 246, 0.03), transparent);
    transition: var(--transition-slow);
    opacity: 0;
}

.professional-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--shadow-xl);
    border-color: var(--accent-blue);
}

.professional-card:hover::after {
    opacity: 1;
    animation: rotate 3s linear infinite;
}

.professional-card h3 {
    color: var(--primary-blue);
    margin-bottom: 1.5rem;
    font-weight: 800;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    position: relative;
    z-index: 2;
}

/* Zone d'upload moderne et attractive */
.upload-zone-modern {
    background: linear-gradient(135deg, var(--bg-secondary) 0%, #f1f5f9 100%);
    border: 3px dashed var(--accent-blue);
    border-radius: var(--radius-xl);
    padding: 4rem 2rem;
    text-align: center;
    margin: 2rem 0;
    transition: var(--transition-normal);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.upload-zone-modern::before {
    content: '📁';
    font-size: 5rem;
    display: block;
    margin-bottom: 1.5rem;
    opacity: 0.8;
    animation: float 4s ease-in-out infinite;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.upload-zone-modern::after {
    content: 'Glissez vos fichiers ici ou cliquez pour parcourir';
    display: block;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 1rem;
}

.upload-zone-modern:hover {
    border-color: var(--primary-orange);
    background: linear-gradient(135deg, #fefbf3 0%, #fef3c7 100%);
    transform: scale(1.02);
    box-shadow: var(--shadow-lg);
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-10px) rotate(2deg); }
    75% { transform: translateY(-5px) rotate(-2deg); }
}

/* File uploader custom styling */
.stFileUploader {
    background: transparent !important;
    border: none !important;
}

.stFileUploader > div {
    background: var(--bg-primary) !important;
    border: 2px solid var(--border-light) !important;
    border-radius: var(--radius-lg) !important;
    padding: 2rem !important;
    transition: var(--transition-normal) !important;
}

.stFileUploader > div:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px);
}

/* Boutons institutionnels premium */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--secondary-blue) 50%, var(--primary-orange) 100%) !important;
    color: var(--text-white) !important;
    border: none !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: var(--transition-normal) !important;
    box-shadow: var(--shadow-lg) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.75px !important;
    position: relative !important;
    overflow: hidden !important;
    border: 2px solid transparent !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: var(--transition-fast);
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: var(--shadow-xl) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:active {
    transform: translateY(-2px) scale(1.02) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--success-green) 0%, #047857 100%) !important;
    color: var(--text-white) !important;
    border: none !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 2rem !important;
    font-weight: 700 !important;
    transition: var(--transition-normal) !important;
    box-shadow: var(--shadow-md) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px) scale(1.05) !important;
    box-shadow: var(--shadow-lg) !important;
    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
}

/* Messages de statut premium */
.status-success {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    color: #065f46;
    padding: 2rem 2.5rem;
    border-radius: var(--radius-xl);
    border-left: 6px solid var(--success-green);
    margin: 2rem 0;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: var(--transition-normal);
    position: relative;
    overflow: hidden;
}

.status-success::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100px;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(5, 150, 105, 0.1));
    animation: shimmer 3s ease-in-out infinite;
}

.status-warning {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    color: #92400e;
    padding: 2rem 2.5rem;
    border-radius: var(--radius-xl);
    border-left: 6px solid var(--warning-yellow);
    margin: 2rem 0;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.status-error {
    background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    color: #991b1b;
    padding: 2rem 2.5rem;
    border-radius: var(--radius-xl);
    border-left: 6px solid var(--error-red);
    margin: 2rem 0;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

@keyframes shimmer {
    0%, 100% { transform: translateX(-100px); opacity: 0; }
    50% { transform: translateX(0); opacity: 1; }
}

/* Métriques institutionnelles redesignées */
.metric-card-institutional {
    background: var(--bg-primary);
    padding: 2.5rem;
    border-radius: var(--radius-xl);
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-lg);
    text-align: center;
    transition: var(--transition-normal);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.metric-card-institutional::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, var(--accent-blue) 0%, var(--primary-orange) 100%);
}

.metric-card-institutional::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    transition: var(--transition-normal);
    transform: translate(-50%, -50%);
}

.metric-card-institutional:hover {
    transform: translateY(-8px) scale(1.05);
    box-shadow: var(--shadow-xl);
    border-color: var(--accent-blue);
}

.metric-card-institutional:hover::after {
    width: 200%;
    height: 200%;
}

.metric-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: block;
    transition: var(--transition-normal);
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.metric-card-institutional:hover .metric-icon {
    transform: scale(1.2) rotate(10deg);
}

.metric-title {
    color: var(--primary-blue);
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-description {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.6;
    font-weight: 500;
}

/* Inputs professionnels */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div > select {
    border-radius: var(--radius-lg) !important;
    border: 2px solid var(--border-light) !important;
    transition: var(--transition-normal) !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
    outline: none !important;
    transform: translateY(-2px) !important;
}

/* Progress bar institutionnelle */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-blue) 0%, var(--primary-orange) 100%) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stProgress > div > div > div::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: progress-shine 2s ease-in-out infinite;
}

@keyframes progress-shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Formulaires */
.stForm {
    background: var(--bg-primary) !important;
    padding: 2.5rem !important;
    border-radius: var(--radius-xl) !important;
    border: 1px solid var(--border-light) !important;
    box-shadow: var(--shadow-lg) !important;
    margin: 2rem 0 !important;
    transition: var(--transition-normal) !important;
}

.stForm:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--shadow-xl) !important;
    transform: translateY(-2px) !important;
}
            
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input,
.stSelectbox>div>div>select {
    border-radius: var(--radius-lg) !important;
    border: 2px solid var(--border-light) !important;
    transition: var(--transition-normal) !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus,
.stNumberInput>div>div>input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15) !important;
    outline: none !important;
    transform: translateY(-2px) !important;
}

/* Labels des formulaires */
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label,
.stRadio label,
.stCheckbox label,
.stSlider label,
.stDateInput label,
.stTimeInput label {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

.stForm .stButton>button {
    width: 100% !important;
    margin-top: 1.5rem !important;
    padding: 1.2rem !important;
    font-size: 1.2rem !important;
}                       

/* Footer institutionnel */
.institutional-footer {
    background: linear-gradient(135deg, var(--primary-blue) 0%, var(--text-dark) 100%);
    color: var(--text-white);
    padding: 3rem 2rem;
    border-radius: var(--radius-xl);
    margin-top: 4rem;
    text-align: center;
    box-shadow: var(--shadow-xl);
}

.footer-logos {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
}

.footer-text {
    opacity: 0.9;
    font-size: 1rem;
    line-height: 1.8;
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1024px) {
    .header-content {
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }
    
    .header-text h1 {
        font-size: 2.5rem;
    }
}

@media (max-width: 768px) {
    .institutional-header {
        padding: 2rem 1.5rem;
    }
    
    .header-text h1 {
        font-size: 2rem;
    }
    
    .professional-card {
        padding: 2rem;
    }
    
    .metric-card-institutional {
        padding: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 1rem;
        font-size: 1rem;
    }
}

/* Scrollbar personnalisée */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg-tertiary);
    border-radius: var(--radius-lg);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent-blue) 0%, var(--primary-orange) 100%);
    border-radius: var(--radius-lg);
    border: 2px solid var(--bg-tertiary);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--secondary-blue) 0%, var(--secondary-orange) 100%);
}

/* Animations d'entrée */
@keyframes slideInFromTop {
    0% { 
        transform: translateY(-100px); 
        opacity: 0; 
    }
    100% { 
        transform: translateY(0); 
        opacity: 1; 
    }
}

@keyframes fadeInScale {
    0% { 
        transform: scale(0.9); 
        opacity: 0; 
    }
    100% { 
        transform: scale(1); 
        opacity: 1; 
    }
}

@keyframes slideInFromLeft {
    0% { 
        transform: translateX(-50px); 
        opacity: 0; 
    }
    100% { 
        transform: translateX(0); 
        opacity: 1; 
    }
}

.professional-card {
    animation: fadeInScale 0.6s ease-out;
}

.institutional-header {
    animation: slideInFromTop 1s ease-out;
}

.metric-card-institutional {
    animation: slideInFromLeft 0.8s ease-out;
}

/* Effets spéciaux pour l'engagement */
.stButton > button:hover {
    animation: pulse 0.6s ease-in-out;
}

@keyframes pulse {
    0%, 100% { transform: translateY(-4px) scale(1.05); }
    50% { transform: translateY(-6px) scale(1.08); }
}

/* Custom select boxes */
.stSelectbox > div > div {
    background: var(--bg-primary) !important;
    border: 2px solid var(--border-light) !important;
    border-radius: var(--radius-lg) !important;
    transition: var(--transition-normal) !important;
}

.stSelectbox > div > div:hover {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--shadow-md) !important;
}

/* Image styling */
img {
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    transition: var(--transition-normal) !important;
}

img:hover {
    transform: scale(1.02) !important;
    box-shadow: var(--shadow-lg) !important;
}
</style>
""", unsafe_allow_html=True)

# Header institutionnel avec logos
st.markdown("""
<div class="institutional-header">
    <div class="header-content">
        <div class="header-logos">
            <div class="logo-container">
                <img src="https://www.etudiant.ma/_next/image?url=https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fetudiant-edce4.firebasestorage.app%2Fo%2Fetudiant-prod%252Fuploads%252Fentity%252Fcover%252F1286%252Fensat.png%3Falt%3Dmedia&w=1920&q=75" alt="ENSAT Logo">
            </div>
            <div class="logo-container">
                <img src="logo_uae_H.png" alt="UAE Logo">
            </div>
        </div>
        <div class="header-text">
            <h1>🎓 Smart Scanner System</h1>
            <p>École Nationale des Sciences Appliquées de Tanger</p>
            <div class="institution-badge">Système Intelligent de Numérisation</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation avec tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Accueil", "📄 PDF Scanner", "📊 Excel Generator", "👥 Group Manager"])

with tab1:
    # Section des métriques institutionnelles
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card-institutional">
            <span class="metric-icon">📄</span>
            <div class="metric-title">PDF Scanner</div>
            <div class="metric-description">Conversion intelligente d'images en PDF</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card-institutional">
            <span class="metric-icon">📊</span>
            <div class="metric-title">Excel Generator</div>
            <div class="metric-description">Extraction automatique de tableaux vers Excel</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card-institutional">
            <span class="metric-icon">📋</span>
            <div class="metric-title">Attendance</div>
            <div class="metric-description">Génération de feuilles de présence personnalisées</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card-institutional">
            <span class="metric-icon">👥</span>
            <div class="metric-title">Groups</div>
            <div class="metric-description">Organisation automatique des groupes</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="professional-card">
            <h3>🎯 Fonctionnalités Principales</h3>
            <ul style="line-height: 2; font-size: 1.1rem;">
                <li><strong>📄 PDF Scanner Avancé</strong> - Technologie OCR de pointe pour une conversion précise</li>
                <li><strong>📊 Extraction Intelligente</strong> - Reconnaissance automatique des structures tabulaires</li>
                <li><strong>📋 Gestion Administrative</strong> - Outils adaptés aux besoins académiques</li>
                <li><strong>👥 Organisation Pédagogique</strong> - Formation de groupes optimisée</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="professional-card">
            <h3>⚡ Avantages Technologiques</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981; font-size: 1.2rem;">✅</span>
                    <span>Traitement haute performance</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981; font-size: 1.2rem;">✅</span>
                    <span>Interface intuitive et moderne</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981; font-size: 1.2rem;">✅</span>
                    <span>Formats multiples supportés</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981; font-size: 1.2rem;">✅</span>
                    <span>Qualité professionnelle garantie</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # st.markdown("""
        # <div class="status-warning">
        #     <span style="font-size: 1.5rem;">💡</span>
        #     <div>
        #         <strong>Conseil Professionnel</strong><br>
        #         Utilisez des images haute résolution et bien éclairées pour des résultats optimaux.
        #     </div>
        # </div>
        # """, unsafe_allow_html=True)
        
        # st.markdown("""
        # <div class="status-success">
        #     <span style="font-size: 1.5rem;">🚀</span>
        #     <div>
        #         <strong>Dernières Améliorations</strong><br>
        #         • Support du français renforcé<br>
        #         • Détection automatique d'orientation<br>
        #         • Interface utilisateur repensée
        #     </div>
        # </div>
        # """, unsafe_allow_html=True)
        
        # Statistiques d'utilisation
        st.markdown("""
        <div class="professional-card">
            <h3>📈 Statistiques d'Utilisation</h3>
            <div style="margin-top: 1.5rem;">
                <div style="margin-bottom: 1.2rem; padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 4px solid #1e3a8a;">
                    <div style="color: #6b7280; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.3rem;">Documents Traités</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #1e3a8a;">1,247</div>
                </div>
                <div style="margin-bottom: 1.2rem; padding: 1rem; background: #f0fdf4; border-radius: 8px; border-left: 4px solid #10b981;">
                    <div style="color: #6b7280; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.3rem;">Tableaux Extraits</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #10b981;">892</div>
                </div>
                <div style="padding: 1rem; background: #fefbf3; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <div style="color: #6b7280; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.3rem;">Taux de Réussite</div>
                    <div style="font-size: 2rem; font-weight: 700; color: #f59e0b;">97.3%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown(
    """
    <div style=" color: white; padding: 12px; border-radius: 8px; font-size: 34px;">
        📄 Convertisseur Image vers PDF
    </div>
    """,
    unsafe_allow_html=True
)


    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-zone-modern">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Glissez votre image ici ou cliquez pour parcourir",
            type=['png', 'jpg', 'jpeg'],
            help="Formats pris en charge: PNG, JPG, JPEG (Taille max: 200MB)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            st.image(uploaded_file, caption="Aperçu de l'image téléchargée", use_container_width=True)
            
            # Informations détaillées sur le fichier
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
            st.markdown(f"""
            <div class="professional-card">
                <h3>📄 Informations du Fichier</h3>
                <p><strong>Nom:</strong> {uploaded_file.name}</p>
                <p><strong>Taille:</strong> {file_size:.2f} MB</p>
                <p><strong>Type:</strong> {uploaded_file.type}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if uploaded_file:
            st.markdown("### ⚙️ Options de traitement")
            
            # Options améliorées
            quality = st.select_slider(
                "Qualité OCR",
                options=["Rapide", "Standard", "Précis", "Ultra"],
                value="Standard",
                help="Rapide: traitement accéléré | Standard: équilibre qualité/vitesse | Précis: haute précision | Ultra: qualité maximale"
            )
            
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                add_background = st.checkbox("Conserver l'image", value=True)
                enhance_contrast = st.checkbox("Améliorer le contraste", value=False)
            
            with col_opt2:
                auto_rotate = st.checkbox("Rotation automatique", value=True)
                compress_pdf = st.checkbox("Compression PDF", value=True)
            
            # Progress bar placeholder
            progress_placeholder = st.empty()
            
            if st.button("🔄 Générer PDF", key="pdf_gen", type="primary"):
                progress_bar = progress_placeholder.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📤 Upload en cours...")
                    progress_bar.progress(20)
                    
                    # Sauvegarder temporairement
                    temp_path = os.path.join("temp_uploads", uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    status_text.text("🔍 Analyse de l'image...")
                    progress_bar.progress(50)
                    
                    # Générer PDF
                    output_path = os.path.join("generated_files", f"document_{uploaded_file.name.split('.')[0]}.pdf")
                    
                    status_text.text("📄 Génération du PDF...")
                    progress_bar.progress(80)
                    
                    result_path = create_searchable_pdf(temp_path, output_path, quality, add_background)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Traitement terminé!")
                    
                    if result_path and os.path.exists(result_path):
                        st.markdown('<div style="color: white; ">✅ PDF généré avec succès!</div>', unsafe_allow_html=True) 
                        
                        # Statistiques du fichier
                        file_size = os.path.getsize(result_path) / (1024 * 1024)
                        st.info(f"📊 Taille du PDF: {file_size:.1f} MB")
                        
                        with open(result_path, "rb") as file:
                            st.download_button(
                                label="📥 Télécharger PDF",
                                data=file.read(),
                                file_name=os.path.basename(result_path),
                                mime="application/pdf",
                                type="secondary"
                            )
                    else:
                        st.markdown('<div class="error-box">❌ Erreur lors de la génération du PDF</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
                finally:
                    progress_placeholder.empty()

with tab3:
    st.markdown(
        """
        <div style="color: white; padding: 12px; border-radius: 8px; font-size: 34px;">
            📊 <strong>Extracteur de Tableaux vers Excel</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="color: white; padding: 12px; border-radius: 8px; font-size: 24px;">
            🎯 <strong>Type de Conversion</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ✅ Boîte d'info élégante
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 12px; border-left: 5px solid #4a90e2;
                    border-radius: 8px; margin-bottom: 10px; color: #333;">
            <strong>🛠️ Choisissez le type de conversion :</strong><br>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ✅ Selectbox simple et aligné
    conversion_type = st.selectbox(
        "",
        [
            "📋 Liste d'absence",
            "📊 Autres listes"
        ]
    )

    # ✅ Séparation visuelle
    st.markdown("<hr style='border: 1px solid #555;'>", unsafe_allow_html=True)

    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
        table_image = st.file_uploader(
            "Image à traiter",
            type=['png', 'jpg', 'jpeg'],
            key="excel_upload",
            help="Choisissez une image selon le type de conversion sélectionné"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if table_image:
            st.image(table_image, caption="Image à traiter", use_container_width=True)
            
            # Informations sur le fichier
            file_size = len(table_image.getvalue()) / (1024 * 1024)  # MB
            st.info(f"📊 **{table_image.name}** ({file_size:.1f} MB)")
    
    with col2:
        if table_image:
            # ✅ NOUVEAU: Paramètres conditionnels selon le type
            if "Autres listes" in conversion_type:
                st.markdown("### ⚙️ Paramètres d'extraction OCR")
                
                # Paramètres avancés pour extraction de tableau
                detection_mode = st.selectbox(
                    "Mode de détection",
                    ["Automatique", "Tableau structuré", "Données libres"],
                    help="Automatique: détection intelligente | Structuré: lignes et colonnes | Libre: extraction de toutes les données"
                )
                
                col_param1, col_param2 = st.columns(2)
                with col_param1:
                    add_styling = st.checkbox("Style professionnel", value=True)
                    add_headers = st.checkbox("Détecter les en-têtes", value=True)
                
                with col_param2:
                    clean_data = st.checkbox("Nettoyer les données", value=True)
                    auto_resize = st.checkbox("Ajuster colonnes", value=True)
                
                # Options avancées
                with st.expander("🔧 Options avancées"):
                    sensitivity = st.slider("Sensibilité OCR", 0.1, 1.0, 0.7, 0.1)
                    min_confidence = st.slider("Confiance minimale", 0.1, 1.0, 0.6, 0.1)
                
                button_text = "📊 Extraire Tableau vers Excel"
                
            elif "Liste d'abssence" in conversion_type:
                st.markdown("### 📸 Paramètres de scan")
                
                col_param1, col_param2 = st.columns(2)
                with col_param1:
                    resize_image = st.checkbox("Redimensionner l'image", value=True)
                    image_quality = st.slider("Qualité d'image", 0.1, 1.0, 0.8, 0.1)
                
                with col_param2:
                    add_border = st.checkbox("Ajouter une bordure", value=False)
                    center_image = st.checkbox("Centrer l'image", value=True)
                
                button_text = "📊 Extraire Tableau vers Excel"
                
           
            
            progress_placeholder = st.empty()
            
            if st.button(button_text, key="process_btn", type="primary"):
                progress_bar = progress_placeholder.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📤 Préparation de l'image...")
                    progress_bar.progress(20)
                    
                    # Sauvegarder temporairement
                    temp_path = os.path.join("temp_uploads", table_image.name)
                    with open(temp_path, "wb") as f:
                        f.write(table_image.getvalue())
                    
                    # ✅ LOGIQUE CONDITIONNELLE selon le type
                    if "Extraction de tableau" in conversion_type:
                        status_text.text("🔍 Extraction OCR du tableau...")
                        progress_bar.progress(50)
                        
                        output_path = os.path.join("generated_files", f"tableau_{table_image.name.split('.')[0]}.xlsx")
                        
                        status_text.text("📊 Génération de l'Excel...")
                        progress_bar.progress(80)
                        st.info("🧠 Mode utilisé : OCR avancé avec EasyOCR")
                        
                        # Utiliser votre fonction OCR existante
                        result_path = image_to_excel_converter(
                            image_path=temp_path,
                            output_path=output_path
                        )
                        
                    elif "Scan simple" in conversion_type:
                        status_text.text("📸 Insertion de l'image...")
                        progress_bar.progress(60)
                        
                        output_path = os.path.join("generated_files", f"scan_{table_image.name.split('.')[0]}.xlsx")
                        
                        # ✅ NOUVEAU: Utiliser votre fonction d'insertion d'image
                        from openpyxl import Workbook
                        from openpyxl.drawing.image import Image as XLImage
                        
                        def insert_image_into_excel_local(image_path, output_excel_path):
                            wb = Workbook()
                            ws = wb.active
                            ws.title = "Image Scannée"
                            
                            img = XLImage(image_path)
                            
                            # Redimensionner si demandé
                            if resize_image:
                                img.width = img.width * image_quality
                                img.height = img.height * image_quality
                            
                            ws.add_image(img, 'A1')
                            wb.save(output_excel_path)
                            return output_excel_path
                        
                        result_path = insert_image_into_excel_local(temp_path, output_path)
                        
                    else:  # Liste d'absence - scan rapide
                        status_text.text("📋 Scan rapide de la liste...")
                        progress_bar.progress(50)
                        
                        output_path = os.path.join("generated_files", f"liste_absence_{table_image.name.split('.')[0]}.xlsx")
                        
                        status_text.text("📊 Formatage de la liste...")
                        progress_bar.progress(80)
                        
                        
                        # Mode rapide avec logique simplifiée
                        result_path = image_to_excel_converter(
                            image_path=temp_path,
                            output_path=output_path
                        )
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Traitement terminé!")
                    
                    if result_path and os.path.exists(result_path):
                        st.markdown('<div class="success-box">✅ Fichier généré avec succès!</div>', unsafe_allow_html=True)
                        
                        # Statistiques
                        file_size = os.path.getsize(result_path) / 1024  # KB
                        st.info(f"📊 Taille du fichier: {file_size:.1f} KB")
                        
                        with open(result_path, "rb") as file:
                            st.download_button(
                                label="📥 Télécharger Excel",
                                data=file.read(),
                                file_name=os.path.basename(result_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                type="secondary"
                            )
                    else:
                        st.markdown('<div class="error-box">❌ Erreur lors du traitement. Vérifiez votre image.</div>', unsafe_allow_html=True)
                        
                        # Conseils selon le type
                        if "Extraction de tableau" in conversion_type:
                            with st.expander("💡 Conseils pour l'extraction de tableau"):
                                st.markdown("""
                                - Assurez-vous que le tableau a des bordures visibles
                                - Vérifiez le contraste entre texte et arrière-plan
                                - Évitez les images floues
                                - Le tableau doit être bien structuré
                                """)
                        elif "Liste d'absence" in conversion_type:
                            with st.expander("💡 Conseils pour les listes d'absence"):
                                st.markdown("""
                                - La liste doit être claire et lisible
                                - Un nom par ligne de préférence
                                - Évitez les écritures manuscrites illisibles
                                - Bonne résolution d'image recommandée
                                """)
                        
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
                finally:
                    progress_placeholder.empty()

with tab4:
    
    st.markdown(
        """
        <div style="color: white; padding: 12px; border-radius: 8px; font-size: 34px;">
            👥 Générateur de Groupes d'Étudiants</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
        """
        <div style="color: white; padding: 12px; border-radius: 8px; font-size: 28px;">
            📝 Feuille de Présence</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
        
        with st.form("attendance_form"):
            class_name = st.text_input(
                "Nom de la classe", 
                value="GI-S5", 
                placeholder="Ex: GI-S5, RT-S3...",
                help="Identifiant de la classe ou du groupe"
            )
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                num_sessions = st.number_input("Nombre de séances", min_value=1, max_value=20, value=6)
            with col_form2:
                num_students = st.number_input("Nombre d'étudiants", min_value=5, max_value=100, value=30)
            
            # Options supplémentaires
            include_notes = st.checkbox("Inclure une colonne notes", value=False)
            custom_header = st.text_input("En-tête personnalisé", placeholder="Université/École...")
            
            submitted = st.form_submit_button("📄 Générer Feuille de Présence", type="primary")
            
            if submitted:
                with st.spinner("📋 Génération de la feuille de présence..."):
                    try:
                        output_path = os.path.join("generated_files", f"presence_{class_name}_{num_sessions}seances.pdf")
                        result_path = generate_attendance_pdf(
                            class_name, 
                            num_sessions, 
                            num_students, 
                            output_path,
                            include_notes=include_notes,
                            custom_header=custom_header
                        )
                        
                        if result_path and os.path.exists(result_path):
                            st.markdown('<div class="success-box">✅ Feuille de présence générée avec succès!</div>', unsafe_allow_html=True)
                            
                            with open(result_path, "rb") as file:
                                st.download_button(
                                    label="📥 Télécharger Feuille",
                                    data=file.read(),
                                    file_name=os.path.basename(result_path),
                                                                        mime="application/pdf",
                                    type="secondary"
                                )
                        else:
                            st.markdown('<div class="error-box">❌ Erreur lors de la génération de la feuille</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(
        """
        <div style="color: white; padding: 12px; border-radius: 8px; font-size: 28px;">
            👥 Créateur de Groupes</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

        with st.form("group_form"):
            student_list_text = st.text_area(
                "Liste des étudiants (un par ligne)",
                placeholder="Ex: Fatima BENALI\nYoussef TAZI\nAmine LAMRANI",
                height=200
            )

            group_size = st.number_input("Taille des groupes", min_value=2, max_value=10, value=3)
            file_prefix = st.text_input("Nom de fichier (optionnel)", value="groupes_classe")

            submitted_group = st.form_submit_button("👥 Générer les Groupes", type="primary")

            if submitted_group:
                if not student_list_text.strip():
                    st.markdown('<div class="warning-box">⚠️ Veuillez saisir la liste des étudiants.</div>', unsafe_allow_html=True)
                else:
                    with st.spinner("🔧 Création des groupes..."):
                        try:
                            students = [line.strip() for line in student_list_text.strip().split('\n') if line.strip()]
                            excel_path = os.path.join("generated_files", f"{file_prefix}.xlsx")
                            pdf_path = os.path.join("generated_files", f"{file_prefix}.pdf")
                            
                            # Appel à ta fonction group_maker
                            excel_result, pdf_result = create_student_groups(students, group_size, excel_path, pdf_path)
                            
                            if excel_result and pdf_result:
                                st.markdown('<div class="success-box">✅ Groupes générés avec succès!</div>', unsafe_allow_html=True)
                                
                                col_dl1, col_dl2 = st.columns(2)
                                with col_dl1:
                                    with open(excel_result, "rb") as file:
                                        st.download_button(
                                            label="📊 Télécharger Excel",
                                            data=file.read(),
                                            file_name=os.path.basename(excel_result),
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                            type="secondary"
                                        )
                                with col_dl2:
                                    with open(pdf_result, "rb") as file:
                                        st.download_button(
                                            label="📄 Télécharger PDF",
                                            data=file.read(),
                                            file_name=os.path.basename(pdf_result),
                                            mime="application/pdf",
                                            type="secondary"
                                        )
                            else:
                                st.markdown('<div class="error-box">❌ Impossible de générer les fichiers de groupe.</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
