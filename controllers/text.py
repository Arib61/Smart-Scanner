# import streamlit as st
# import os
# import tempfile
# from PIL import Image
# import base64

# # Import des modules de traitement
# from pdf_creator import create_searchable_pdf
# from image_to_excel_converter_local import image_to_excel_converter_local as image_to_excel_converter
# from attendance_sheet import generate_attendance_pdf
# from group_maker import create_student_groups

# # Configuration
# st.set_page_config(
#     page_title="Smart Scanner System", 
#     page_icon="🔍", 
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Créer les dossiers nécessaires
# for folder in ["temp_uploads", "generated_files", "assets"]:
#     os.makedirs(folder, exist_ok=True)

# # CSS moderne et professionnel
# st.markdown("""
# <style>
#     /* Variables CSS */
#     :root {
#         --primary-color: #2E86AB;
#         --secondary-color: #A23B72;
#         --accent-color: #F18F01;
#         --success-color: #16A085;
#         --warning-color: #F39C12;
#         --error-color: #E74C3C;
#         --dark-bg: #1E1E1E;
#         --light-bg: #F8F9FA;
#         --text-dark: #2C3E50;
#         --text-light: #7F8C8D;
#         --border-radius: 12px;
#         --shadow: 0 4px 20px rgba(0,0,0,0.1);
#         --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#     }
#      /* Forcer le fond de toute l'app en noir */
#     html, body, .main, .block-container {
#         background-color: #1E1E1E !important;
#         color: #F8F9FA !important;
#     }

#     /* Supprimer le fond blanc des composants st-tabs */
#     .stTabs [data-baseweb="tab-list"],
#     .stTabs [data-baseweb="tab"] {
#         background: #2C2C2C !important;
#         color: white !important;
#         border-color: #444 !important;
#     }
#     .stTabs [aria-selected="true"] {
#         background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
#         color: white !important;
#     }
#             /* ✅ Forcer fond noir sur toutes les cartes */
# .feature-card,
# .metric-card,
# .upload-zone,
# .stTabs [data-baseweb="tab"],
# .stTabs [data-baseweb="tab-list"],
# .stMarkdown,
# .stDownloadButton,
# div[data-testid="stForm"],
# .block-container {
#     background-color: #1e1e1e !important;
#     color: #f5f5f5 !important;
#     border-color: #444 !important;
# }

# /* ✅ Forcer texte visible sur fond noir */
# .feature-card *,
# .metric-card *,
# .upload-zone *,
# .stMarkdown *,
# .stDownloadButton *,
# .stTabs *,
# div[data-testid="stForm"] * {
#     color: #f5f5f5 !important;
# }

# /* ✅ Rendre les icônes et métriques bien visibles */
# .metric-value {
#     color: #42A5F5 !important;
# }
# .metric-label {
#     color: #CCCCCC !important;
# }

        
            
            

#     /* Layout principal */
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         max-width: 1200px;
#     }

#     /* Header principal */
#     .main-header {
#         background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
#         padding: 3rem 2rem;
#         border-radius: var(--border-radius);
#         color: white;
#         text-align: center;
#         margin-bottom: 2rem;
#         box-shadow: var(--shadow);
#         position: relative;
#         overflow: hidden;
#     }

#     .main-header::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         bottom: 0;
#         background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a" cx="50%" cy="50%"><stop offset="0%" stop-color="%23fff" stop-opacity="0.1"/><stop offset="100%" stop-color="%23fff" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
#         pointer-events: none;
#     }

#     .main-header h1 {
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 2px 4px rgba(0,0,0,0.3);
#     }

#     .main-header p {
#         font-size: 1.1rem;
#         opacity: 0.9;
#         margin: 0;
#     }

#     /* Cards et conteneurs */
#     .feature-card {
#         background: white;
#         padding: 2rem;
#         border-radius: var(--border-radius);
#         border: 1px solid #E8ECF0;
#         box-shadow: var(--shadow);
#         margin-bottom: 1.5rem;
#         transition: var(--transition);
#         position: relative;
#     }

#     .feature-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 8px 30px rgba(0,0,0,0.15);
#         border-color: var(--primary-color);
#     }

#     .feature-card h3 {
#         color: var(--text-dark);
#         margin-bottom: 1rem;
#         font-weight: 600;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }

#     /* Zone d'upload */
#     .upload-zone {
#         border: 2px dashed var(--primary-color);
#         border-radius: var(--border-radius);
#         padding: 3rem 2rem;
#         text-align: center;
#         background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);
#         margin: 1.5rem 0;
#         transition: var(--transition);
#         position: relative;
#     }

#     .upload-zone:hover {
#         border-color: var(--secondary-color);
#         background: linear-gradient(135deg, #f0f8ff 0%, #e0f2fe 100%);
#     }

#     .upload-zone::before {
#         content: "📁";
#         font-size: 3rem;
#         display: block;
#         margin-bottom: 1rem;
#         opacity: 0.7;
#     }

#     /* Messages de statut */
#     .success-box {
#         background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
#         color: var(--success-color);
#         padding: 1.5rem;
#         border-radius: var(--border-radius);
#         border-left: 4px solid var(--success-color);
#         margin: 1.5rem 0;
#         font-weight: 500;
#         box-shadow: 0 2px 10px rgba(22, 160, 133, 0.1);
#     }

#     .warning-box {
#         background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
#         color: var(--warning-color);
#         padding: 1.5rem;
#         border-radius: var(--border-radius);
#         border-left: 4px solid var(--warning-color);
#         margin: 1.5rem 0;
#         font-weight: 500;
#         box-shadow: 0 2px 10px rgba(243, 156, 18, 0.1);
#     }

#     .error-box {
#         background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
#         color: var(--error-color);
#         padding: 1.5rem;
#         border-radius: var(--border-radius);
#         border-left: 4px solid var(--error-color);
#         margin: 1.5rem 0;
#         font-weight: 500;
#         box-shadow: 0 2px 10px rgba(231, 76, 60, 0.1);
#     }

#     /* Boutons */
#     .stButton > button {
#         background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
#         color: white;
#         border: none;
#         border-radius: var(--border-radius);
#         padding: 0.75rem 2rem;
#         font-weight: 600;
#         font-size: 1rem;
#         transition: var(--transition);
#         box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 25px rgba(46, 134, 171, 0.4);
#         background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
#     }

#     .stButton > button:active {
#         transform: translateY(0);
#     }

#     /* Download buttons */
#     .stDownloadButton > button {
#         background: linear-gradient(135deg, var(--success-color) 0%, #27AE60 100%);
#         color: white;
#         border: none;
#         border-radius: var(--border-radius);
#         padding: 0.75rem 1.5rem;
#         font-weight: 600;
#         transition: var(--transition);
#         box-shadow: 0 4px 15px rgba(22, 160, 133, 0.3);
#     }

#     .stDownloadButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 25px rgba(22, 160, 133, 0.4);
#     }

#     /* Tabs */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 8px;
#         background: var(--light-bg);
#         padding: 0.5rem;
#         border-radius: var(--border-radius);
#         border: 1px solid #E8ECF0;
#     }

#     .stTabs [data-baseweb="tab"] {
#         height: 50px;
#         padding: 0 1.5rem;
#         background: white;
#         border-radius: 8px;
#         border: 1px solid transparent;
#         transition: var(--transition);
#         font-weight: 500;
#     }

#     .stTabs [aria-selected="true"] {
#         background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
#         color: white;
#     }

#     /* Inputs */
#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea,
#     .stNumberInput > div > div > input {
#         border-radius: var(--border-radius);
#         border: 2px solid #E8ECF0;
#         transition: var(--transition);
#         padding: 0.75rem;
#     }

#     .stTextInput > div > div > input:focus,
#     .stTextArea > div > div > textarea:focus,
#     .stNumberInput > div > div > input:focus {
#         border-color: var(--primary-color);
#         box-shadow: 0 0 0 3px rgba(46, 134, 171, 0.1);
#     }

#     /* Select slider */
#     .stSelectSlider > div > div {
#         background: var(--light-bg);
#         border-radius: var(--border-radius);
#         padding: 0.5rem;
#     }

#     /* Checkbox */
#     .stCheckbox > label {
#         font-weight: 500;
#         color: var(--text-dark);
#     }

#     /* Metrics */
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: var(--border-radius);
#         border: 1px solid #E8ECF0;
#         box-shadow: var(--shadow);
#         text-align: center;
#         transition: var(--transition);
#     }

#     .metric-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 8px 25px rgba(0,0,0,0.12);
#     }

#     .metric-value {
#         font-size: 2rem;
#         font-weight: 700;
#         color: var(--primary-color);
#         margin-bottom: 0.5rem;
#     }

#     .metric-label {
#         color: var(--text-light);
#         font-size: 0.9rem;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }

#     /* Footer */
#     .footer {
#         text-align: center;
#         color: var(--text-light);
#         font-size: 0.9rem;
#         padding: 2rem 0;
#         border-top: 1px solid #E8ECF0;
#         margin-top: 3rem;
#     }

#     /* Animations */
#     @keyframes fadeInUp {
#         from {
#             opacity: 0;
#             transform: translateY(20px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }

#     .feature-card {
#         animation: fadeInUp 0.6s ease-out;
#     }

#     /* Responsive */
#     @media (max-width: 768px) {
#         .main-header h1 {
#             font-size: 2rem;
#         }
        
#         .main-header p {
#             font-size: 1rem;
#         }
        
#         .feature-card {
#             padding: 1.5rem;
#         }
        
#         .upload-zone {
#             padding: 2rem 1rem;
#         }
#     }

#     /* Progress bar */
#     .stProgress > div > div > div {
#         background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
#         border-radius: 10px;
#     }

#     /* Spinner */
#     .stSpinner > div {
#         border-color: var(--primary-color) transparent var(--primary-color) transparent;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header principal
# st.markdown("""
# <div class="main-header">
#     <h1>🔍 Smart Scanner System</h1>
#     <p>Système intelligent de numérisation et traitement de documents</p>
# </div>
# """, unsafe_allow_html=True)

# # Navigation avec tabs
# tab1, tab2, tab3, tab4 = st.tabs(["🏠 Accueil", "📄 PDF Scanner", "📊 Excel Generator", "👥 Group Manager"])

# with tab1:
#     # Section des métriques
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">📄</div>
#             <div class="metric-label">PDF Scanner</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">📊</div>
#             <div class="metric-label">Excel Generator</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">📋</div>
#             <div class="metric-label">Attendance</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">👥</div>
#             <div class="metric-label">Groups</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown("""
#         <div class="feature-card">
#             <h3>🎯 Fonctionnalités principales</h3>
#             <ul style="line-height: 1.8;">
#                 <li><strong>PDF Scanner</strong> - Convertit vos images en PDF avec texte recherchable</li>
#                 <li><strong>Excel Generator</strong> - Extrait les tableaux d'images vers Excel</li>
#                 <li><strong>Attendance Sheets</strong> - Génère des feuilles de présence automatiquement</li>
#                 <li><strong>Group Manager</strong> - Organise les étudiants en groupes de travail</li>
#             </ul>
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("""
#         <div class="feature-card">
#             <h3>⚡ Avantages</h3>
#             <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
#                 <div>✅ Traitement rapide et précis</div>
#                 <div>✅ Interface intuitive</div>
#                 <div>✅ Formats multiples supportés</div>
#                 <div>✅ Qualité professionnelle</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.info("💡 **Conseil Professionnel**\n\nUtilisez des images nettes et bien éclairées pour obtenir des résultats optimaux.")
#         st.success("🚀 **Nouveautés**\n\n• Support du français amélioré\n• Détection automatique d'orientation\n• Interface utilisateur repensée")
        
#         # Statistiques d'utilisation fictives
#         st.markdown("""
#         <div class="feature-card">
#             <h3>📈 Statistiques</h3>
#             <div style="margin-top: 1rem;">
#                 <div style="margin-bottom: 0.8rem;">
#                     <span style="color: #7F8C8D;">Documents traités</span><br>
#                     <span style="font-size: 1.5rem; font-weight: 600; color: #2E86AB;">1,247</span>
#                 </div>
#                 <div style="margin-bottom: 0.8rem;">
#                     <span style="color: #7F8C8D;">Tableaux extraits</span><br>
#                     <span style="font-size: 1.5rem; font-weight: 600; color: #16A085;">892</span>
#                 </div>
#                 <div>
#                     <span style="color: #7F8C8D;">Taux de réussite</span><br>
#                     <span style="font-size: 1.5rem; font-weight: 600; color: #27AE60;">97.3%</span>
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

# with tab2:
#     st.markdown("### 📄 Convertisseur Image vers PDF")
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader(
#             "Glissez votre image ici ou cliquez pour parcourir",
#             type=['png', 'jpg', 'jpeg'],
#             help="Formats supportés: PNG, JPG, JPEG (Max: 200MB)"
#         )
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         if uploaded_file:
#             st.image(uploaded_file, caption="Aperçu de l'image", use_container_width=True)
            
#             # Informations sur le fichier
#             file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
#             st.info(f"📄 **{uploaded_file.name}** ({file_size:.1f} MB)")
    
#     with col2:
#         if uploaded_file:
#             st.markdown("### ⚙️ Options de traitement")
            
#             # Options améliorées
#             quality = st.select_slider(
#                 "Qualité OCR",
#                 options=["Rapide", "Standard", "Précis", "Ultra"],
#                 value="Standard",
#                 help="Rapide: traitement accéléré | Standard: équilibre qualité/vitesse | Précis: haute précision | Ultra: qualité maximale"
#             )
            
#             col_opt1, col_opt2 = st.columns(2)
#             with col_opt1:
#                 add_background = st.checkbox("Conserver l'image", value=True)
#                 enhance_contrast = st.checkbox("Améliorer le contraste", value=False)
            
#             with col_opt2:
#                 auto_rotate = st.checkbox("Rotation automatique", value=True)
#                 compress_pdf = st.checkbox("Compression PDF", value=True)
            
#             # Progress bar placeholder
#             progress_placeholder = st.empty()
            
#             if st.button("🔄 Générer PDF", key="pdf_gen", type="primary"):
#                 progress_bar = progress_placeholder.progress(0)
#                 status_text = st.empty()
                
#                 try:
#                     status_text.text("📤 Upload en cours...")
#                     progress_bar.progress(20)
                    
#                     # Sauvegarder temporairement
#                     temp_path = os.path.join("temp_uploads", uploaded_file.name)
#                     with open(temp_path, "wb") as f:
#                         f.write(uploaded_file.getvalue())
                    
#                     status_text.text("🔍 Analyse de l'image...")
#                     progress_bar.progress(50)
                    
#                     # Générer PDF
#                     output_path = os.path.join("generated_files", f"document_{uploaded_file.name.split('.')[0]}.pdf")
                    
#                     status_text.text("📄 Génération du PDF...")
#                     progress_bar.progress(80)
                    
#                     result_path = create_searchable_pdf(temp_path, output_path, quality, add_background)
                    
#                     progress_bar.progress(100)
#                     status_text.text("✅ Traitement terminé!")
                    
#                     if result_path and os.path.exists(result_path):
#                         st.markdown('<div class="success-box">✅ PDF généré avec succès!</div>', unsafe_allow_html=True)
                        
#                         # Statistiques du fichier
#                         file_size = os.path.getsize(result_path) / (1024 * 1024)
#                         st.info(f"📊 Taille du PDF: {file_size:.1f} MB")
                        
#                         with open(result_path, "rb") as file:
#                             st.download_button(
#                                 label="📥 Télécharger PDF",
#                                 data=file.read(),
#                                 file_name=os.path.basename(result_path),
#                                 mime="application/pdf",
#                                 type="secondary"
#                             )
#                     else:
#                         st.markdown('<div class="error-box">❌ Erreur lors de la génération du PDF</div>', unsafe_allow_html=True)
                        
#                 except Exception as e:
#                     st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
#                 finally:
#                     progress_placeholder.empty()

# with tab3:
#     st.markdown("### 📊 Extracteur de Tableaux vers Excel")
    
#     # ✅ NOUVEAU: Sélection du type de conversion
#     st.markdown("### 🎯 Type de Conversion")
#     conversion_type = st.selectbox(
#         "Choisissez le type de conversion :",
#         [
#             "📋 Liste d'abssence",
#             "📊 Autres listes"
#         ],
#         help="Sélectionnez le mode de traitement adapté à votre besoin"
#     )
    
#     st.markdown("---")
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
#         table_image = st.file_uploader(
#             "Image à traiter",
#             type=['png', 'jpg', 'jpeg'],
#             key="excel_upload",
#             help="Choisissez une image selon le type de conversion sélectionné"
#         )
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         if table_image:
#             st.image(table_image, caption="Image à traiter", use_container_width=True)
            
#             # Informations sur le fichier
#             file_size = len(table_image.getvalue()) / (1024 * 1024)  # MB
#             st.info(f"📊 **{table_image.name}** ({file_size:.1f} MB)")
    
#     with col2:
#         if table_image:
#             # ✅ NOUVEAU: Paramètres conditionnels selon le type
#             if "Autres listes" in conversion_type:
#                 st.markdown("### ⚙️ Paramètres d'extraction OCR")
                
#                 # Paramètres avancés pour extraction de tableau
#                 detection_mode = st.selectbox(
#                     "Mode de détection",
#                     ["Automatique", "Tableau structuré", "Données libres"],
#                     help="Automatique: détection intelligente | Structuré: lignes et colonnes | Libre: extraction de toutes les données"
#                 )
                
#                 col_param1, col_param2 = st.columns(2)
#                 with col_param1:
#                     add_styling = st.checkbox("Style professionnel", value=True)
#                     add_headers = st.checkbox("Détecter les en-têtes", value=True)
                
#                 with col_param2:
#                     clean_data = st.checkbox("Nettoyer les données", value=True)
#                     auto_resize = st.checkbox("Ajuster colonnes", value=True)
                
#                 # Options avancées
#                 with st.expander("🔧 Options avancées"):
#                     sensitivity = st.slider("Sensibilité OCR", 0.1, 1.0, 0.7, 0.1)
#                     min_confidence = st.slider("Confiance minimale", 0.1, 1.0, 0.6, 0.1)
                
#                 button_text = "📊 Extraire Tableau vers Excel"
                
#             elif "Liste d'abssence" in conversion_type:
#                 st.markdown("### 📸 Paramètres de scan")
                
#                 col_param1, col_param2 = st.columns(2)
#                 with col_param1:
#                     resize_image = st.checkbox("Redimensionner l'image", value=True)
#                     image_quality = st.slider("Qualité d'image", 0.1, 1.0, 0.8, 0.1)
                
#                 with col_param2:
#                     add_border = st.checkbox("Ajouter une bordure", value=False)
#                     center_image = st.checkbox("Centrer l'image", value=True)
                
#                 button_text = "📊 Extraire Tableau vers Excel"
                
           
            
#             progress_placeholder = st.empty()
            
#             if st.button(button_text, key="process_btn", type="primary"):
#                 progress_bar = progress_placeholder.progress(0)
#                 status_text = st.empty()
                
#                 try:
#                     status_text.text("📤 Préparation de l'image...")
#                     progress_bar.progress(20)
                    
#                     # Sauvegarder temporairement
#                     temp_path = os.path.join("temp_uploads", table_image.name)
#                     with open(temp_path, "wb") as f:
#                         f.write(table_image.getvalue())
                    
#                     # ✅ LOGIQUE CONDITIONNELLE selon le type
#                     if "Extraction de tableau" in conversion_type:
#                         status_text.text("🔍 Extraction OCR du tableau...")
#                         progress_bar.progress(50)
                        
#                         output_path = os.path.join("generated_files", f"tableau_{table_image.name.split('.')[0]}.xlsx")
                        
#                         status_text.text("📊 Génération de l'Excel...")
#                         progress_bar.progress(80)
#                         st.info("🧠 Mode utilisé : OCR avancé avec EasyOCR")
                        
#                         # Utiliser votre fonction OCR existante
#                         result_path = image_to_excel_converter(
#                             image_path=temp_path,
#                             output_path=output_path
#                         )
                        
#                     elif "Scan simple" in conversion_type:
#                         status_text.text("📸 Insertion de l'image...")
#                         progress_bar.progress(60)
                        
#                         output_path = os.path.join("generated_files", f"scan_{table_image.name.split('.')[0]}.xlsx")
                        
#                         # ✅ NOUVEAU: Utiliser votre fonction d'insertion d'image
#                         from openpyxl import Workbook
#                         from openpyxl.drawing.image import Image as XLImage
                        
#                         def insert_image_into_excel_local(image_path, output_excel_path):
#                             wb = Workbook()
#                             ws = wb.active
#                             ws.title = "Image Scannée"
                            
#                             img = XLImage(image_path)
                            
#                             # Redimensionner si demandé
#                             if resize_image:
#                                 img.width = img.width * image_quality
#                                 img.height = img.height * image_quality
                            
#                             ws.add_image(img, 'A1')
#                             wb.save(output_excel_path)
#                             return output_excel_path
                        
#                         result_path = insert_image_into_excel_local(temp_path, output_path)
                        
#                     else:  # Liste d'absence - scan rapide
#                         status_text.text("📋 Scan rapide de la liste...")
#                         progress_bar.progress(50)
                        
#                         output_path = os.path.join("generated_files", f"liste_absence_{table_image.name.split('.')[0]}.xlsx")
                        
#                         status_text.text("📊 Formatage de la liste...")
#                         progress_bar.progress(80)
#                         st.info("🧠 Mode utilisé : OCR avancé avec EasyOCR")
                        
#                         # Mode rapide avec logique simplifiée
#                         result_path = image_to_excel_converter(
#                             image_path=temp_path,
#                             output_path=output_path
#                         )
                    
#                     progress_bar.progress(100)
#                     status_text.text("✅ Traitement terminé!")
                    
#                     if result_path and os.path.exists(result_path):
#                         st.markdown('<div class="success-box">✅ Fichier généré avec succès!</div>', unsafe_allow_html=True)
                        
#                         # Statistiques
#                         file_size = os.path.getsize(result_path) / 1024  # KB
#                         st.info(f"📊 Taille du fichier: {file_size:.1f} KB")
                        
#                         with open(result_path, "rb") as file:
#                             st.download_button(
#                                 label="📥 Télécharger Excel",
#                                 data=file.read(),
#                                 file_name=os.path.basename(result_path),
#                                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                                 type="secondary"
#                             )
#                     else:
#                         st.markdown('<div class="error-box">❌ Erreur lors du traitement. Vérifiez votre image.</div>', unsafe_allow_html=True)
                        
#                         # Conseils selon le type
#                         if "Extraction de tableau" in conversion_type:
#                             with st.expander("💡 Conseils pour l'extraction de tableau"):
#                                 st.markdown("""
#                                 - Assurez-vous que le tableau a des bordures visibles
#                                 - Vérifiez le contraste entre texte et arrière-plan
#                                 - Évitez les images floues
#                                 - Le tableau doit être bien structuré
#                                 """)
#                         elif "Liste d'absence" in conversion_type:
#                             with st.expander("💡 Conseils pour les listes d'absence"):
#                                 st.markdown("""
#                                 - La liste doit être claire et lisible
#                                 - Un nom par ligne de préférence
#                                 - Évitez les écritures manuscrites illisibles
#                                 - Bonne résolution d'image recommandée
#                                 """)
                        
#                 except Exception as e:
#                     st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
#                 finally:
#                     progress_placeholder.empty()

# with tab4:
#     st.markdown("### 👥 Générateur de Groupes d'Étudiants")
    
#     col1, col2 = st.columns([1, 1])
    
#     from attendance_sheet_ocr import generate_attendance_from_image

# # Remplacer la section "Feuille de Présence" dans votre tab4 par ceci :

# with col1:
#     st.markdown("### 📝 Feuille de Présence depuis Image")
    
#     # Upload d'image de liste d'étudiants
#     st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
#     student_list_image = st.file_uploader(
#         "Image de la liste d'étudiants",
#         type=['png', 'jpg', 'jpeg'],
#         key="attendance_image_upload",
#         help="Uploadez une image contenant un tableau avec la liste des étudiants"
#     )
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     if student_list_image:
#         st.image(student_list_image, caption="Liste d'étudiants", use_container_width=True)
        
#         # Informations sur le fichier
#         file_size = len(student_list_image.getvalue()) / (1024 * 1024)  # MB
#         st.info(f"📊 **{student_list_image.name}** ({file_size:.1f} MB)")
    
#     with st.form("attendance_ocr_form"):
#         class_name = st.text_input(
#             "Nom de la classe", 
#             value="GI-S5", 
#             placeholder="Ex: GI-S5, RT-S3...",
#             help="Identifiant de la classe ou du groupe"
#         )
        
#         col_form1, col_form2 = st.columns(2)
#         with col_form1:
#             num_sessions = st.number_input("Nombre de séances", min_value=1, max_value=20, value=6)
#             output_format = st.selectbox("Format de sortie", ["PDF", "Excel"], index=0)
            
#         with col_form2:
#             include_notes = st.checkbox("Inclure une colonne notes", value=False)
#             custom_header = st.text_input("En-tête personnalisé", placeholder="Université/École...")
        
#         # Options avancées
#         with st.expander("🔧 Options avancées OCR"):
#             st.info("⚙️ Ces paramètres affectent la qualité d'extraction du texte depuis l'image")
#             ocr_quality = st.selectbox(
#                 "Qualité OCR", 
#                 ["Standard", "Haute précision", "Rapide"], 
#                 index=0,
#                 help="Standard: équilibre vitesse/précision | Haute précision: meilleur pour texte complexe | Rapide: traitement accéléré"
#             )
            
#             preprocess_image = st.checkbox("Prétraitement d'image", value=True, 
#                                          help="Améliore la qualité avant OCR")
        
#         submitted = st.form_submit_button("📄 Générer Feuille de Présence", type="primary")
        
#         if submitted:
#             if not student_list_image:
#                 st.markdown('<div class="warning-box">⚠️ Veuillez uploader une image de la liste d\'étudiants.</div>', unsafe_allow_html=True)
#             else:
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
                
#                 try:
#                     status_text.text("📤 Sauvegarde de l'image...")
#                     progress_bar.progress(20)
                    
#                     # Sauvegarder temporairement l'image
#                     temp_path = os.path.join("temp_uploads", student_list_image.name)
#                     with open(temp_path, "wb") as f:
#                         f.write(student_list_image.getvalue())
                    
#                     status_text.text("🔍 Extraction OCR en cours...")
#                     progress_bar.progress(50)
                    
#                     status_text.text("📋 Génération de la feuille de présence...")
#                     progress_bar.progress(80)
                    
#                     # Générer la feuille de présence
#                     result_path = generate_attendance_from_image(
#                         image_path=temp_path,
#                         class_name=class_name,
#                         num_sessions=num_sessions,
#                         output_format=output_format.lower(),
#                         include_notes=include_notes,
#                         custom_header=custom_header
#                     )
                    
#                     progress_bar.progress(100)
#                     status_text.text("✅ Traitement terminé!")
                    
#                     if result_path and os.path.exists(result_path):
#                         st.markdown('<div class="success-box">✅ Feuille de présence générée avec succès!</div>', unsafe_allow_html=True)
                        
#                         # Statistiques du fichier
#                         file_size = os.path.getsize(result_path) / (1024 * 1024) if output_format.lower() == "pdf" else os.path.getsize(result_path) / 1024
#                         unit = "MB" if output_format.lower() == "pdf" else "KB"
#                         st.info(f"📊 Taille du fichier: {file_size:.1f} {unit}")
                        
#                         # Informations sur l'extraction
#                         with st.expander("📋 Détails de l'extraction"):
#                             st.success("✅ Extraction OCR réussie")
#                             st.info("ℹ️ Les étudiants ont été automatiquement détectés depuis l'image du tableau")
#                             if custom_header:
#                                 st.info(f"📝 En-tête personnalisé ajouté : {custom_header}")
                        
#                         # Bouton de téléchargement
#                         mime_type = "application/pdf" if output_format.lower() == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        
#                         with open(result_path, "rb") as file:
#                             st.download_button(
#                                 label=f"📥 Télécharger {output_format.upper()}",
#                                 data=file.read(),
#                                 file_name=os.path.basename(result_path),
#                                 mime=mime_type,
#                                 type="secondary"
#                             )
#                     else:
#                         st.markdown('<div class="error-box">❌ Erreur lors de la génération de la feuille</div>', unsafe_allow_html=True)
                        
#                         # Conseils de résolution de problème
#                         with st.expander("💡 Conseils de dépannage"):
#                             st.markdown("""
#                             **Si l'extraction a échoué, vérifiez :**
#                             - L'image contient bien un tableau structuré
#                             - Le texte est lisible et contrasté
#                             - L'image n'est pas floue ou déformée
#                             - Le tableau a des bordures visibles
#                             - Les noms sont clairement séparés
#                             """)
                        
#                 except Exception as e:
#                     st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
                    
#                     # Debug info
#                     if "Aucune donnée extraite" in str(e):
#                         st.warning("🔍 **Problème de détection de tableau**\n\nL'OCR n'a pas pu détecter de structure de tableau dans votre image. Assurez-vous que l'image contient un tableau avec des bordures claires.")
#                     elif "Aucun étudiant identifié" in str(e):
#                         st.warning("👥 **Problème d'identification des étudiants**\n\nLe tableau a été détecté mais les noms d'étudiants n'ont pas pu être extraits. Vérifiez la qualité du texte dans l'image.")
                
#                 finally:
#                     # Nettoyer
#                     st.empty()
#     with col2:
#         st.markdown("### 👥 Créateur de Groupes")

#         with st.form("group_form"):
#             student_list_text = st.text_area(
#                 "Liste des étudiants (un par ligne)",
#                 placeholder="Ex: Fatima BENALI\nYoussef TAZI\nAmine LAMRANI",
#                 height=200
#             )

#             group_size = st.number_input("Taille des groupes", min_value=2, max_value=10, value=3)
#             file_prefix = st.text_input("Nom de fichier (optionnel)", value="groupes_classe")

#             submitted_group = st.form_submit_button("👥 Générer les Groupes", type="primary")

#             if submitted_group:
#                 if not student_list_text.strip():
#                     st.markdown('<div class="warning-box">⚠️ Veuillez saisir la liste des étudiants.</div>', unsafe_allow_html=True)
#                 else:
#                     with st.spinner("🔧 Création des groupes..."):
#                         try:
#                             students = [line.strip() for line in student_list_text.strip().split('\n') if line.strip()]
#                             excel_path = os.path.join("generated_files", f"{file_prefix}.xlsx")
#                             pdf_path = os.path.join("generated_files", f"{file_prefix}.pdf")
                            
#                             # Appel à ta fonction group_maker
#                             excel_result, pdf_result = create_student_groups(students, group_size, excel_path, pdf_path)
                            
#                             if excel_result and pdf_result:
#                                 st.markdown('<div class="success-box">✅ Groupes générés avec succès!</div>', unsafe_allow_html=True)
                                
#                                 col_dl1, col_dl2 = st.columns(2)
#                                 with col_dl1:
#                                     with open(excel_result, "rb") as file:
#                                         st.download_button(
#                                             label="📊 Télécharger Excel",
#                                             data=file.read(),
#                                             file_name=os.path.basename(excel_result),
#                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                                             type="secondary"
#                                         )
#                                 with col_dl2:
#                                     with open(pdf_result, "rb") as file:
#                                         st.download_button(
#                                             label="📄 Télécharger PDF",
#                                             data=file.read(),
#                                             file_name=os.path.basename(pdf_result),
#                                             mime="application/pdf",
#                                             type="secondary"
#                                         )
#                             else:
#                                 st.markdown('<div class="error-box">❌ Impossible de générer les fichiers de groupe.</div>', unsafe_allow_html=True)
#                         except Exception as e:
#                             st.markdown(f'<div class="error-box">❌ Erreur: {str(e)}</div>', unsafe_allow_html=True)
