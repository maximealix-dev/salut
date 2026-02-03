# app.py ── LA LANGUE D'INTERNET ── Version finale TikTok + IA + Recherche + Tout ── février 2026

import streamlit as st
import json
import os
import time
from datetime import datetime
import random

# ==================== CONFIG & DATA ====================
DATA_FILE = "langue_internet.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "words": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
users = data["users"]
words = data["words"]

# ==================== SESSION STATE ====================
if "user" not in st.session_state:
    st.session_state.user = None
if "words" not in st.session_state:
    st.session_state.words = words
if "last_sync" not in st.session_state:
    st.session_state.last_sync = time.time()
if "edit_idx" not in st.session_state:
    st.session_state.edit_idx = None
if "delete_idx" not in st.session_state:
    st.session_state.delete_idx = None

# ==================== STYLE TIKTOK ULTRA CLEAN ====================
st.set_page_config(page_title="🌐 La Langue d'Internet", page_icon="🌐", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;600;900&display=swap');
    
    body { background: #000; color: white; }
    .titre { 
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4.2rem; 
        background: linear-gradient(90deg, #fe2c55, #25f4ee, #a033ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0 1rem;
        text-shadow: 0 0 30px rgba(254,44,85,0.5);
    }
    .card {
        background: rgba(20,20,40,0.95);
        border-radius: 20px;
        padding: 1.6rem;
        margin: 1rem auto;
        max-width: 650px;
        border: 1px solid #fe2c5566;
        box-shadow: 0 10px 30px rgba(254,44,85,0.2);
        backdrop-filter: blur(10px);
    }
    .emoji { font-size: 4.5rem; text-align: center; margin: 0.5rem 0; }
    .word { font-size: 2.4rem; text-align: center; font-weight: 900; color: #25f4ee; }
    .def { font-size: 1.2rem; text-align: center; line-height: 1.6; color: #e0e0ff; margin: 1rem 0; }
    .tag { display: inline-block; background: #fe2c55; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; margin: 0.3rem; }
    .author { text-align: center; color: #aaa; font-size: 0.9rem; margin-top: 0.8rem; }
    .btn-ia { background: linear-gradient(90deg, #a033ff, #fe2c55); border: none; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">🌐 LA LANGUE D\'INTERNET</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ccc; font-size:1.2rem;'>Crée, partage et traduis la langue du futur avec tes potes 🔥</p>", unsafe_allow_html=True)

# ==================== CONNEXION / INSCRIPTION ====================
if not st.session_state.user:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Connexion")
        login_user = st.text_input("Pseudo", key="login_user")
        login_pass = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("Se connecter", type="primary"):
            if login_user in users and users[login_user]["password"] == login_pass:
                st.session_state.user = login_user
                st.success(f"Bienvenue {login_user} !")
                st.rerun()
            else:
                st.error("Mauvais pseudo ou mot de passe")
    
    with col2:
        st.subheader("Inscription")
        new_user = st.text_input("Nouveau pseudo", key="new_user")
        new_pass = st.text_input("Mot de passe", type="password", key="new_pass")
        if st.button("Créer mon compte"):
            if new_user in users:
                st.error("Pseudo déjà pris")
            elif len(new_user) < 3:
                st.error("Pseudo trop court")
            else:
                users[new_user] = {"password": new_pass}
                save_data({"users": users, "words": st.session_state.words})
                st.success("Compte créé ! Connecte-toi")
                st.rerun()
    st.stop()

# ==================== AJOUT DE MOT + IA ====================
st.subheader("Crée un nouveau mot")

with st.form("add_word", clear_on_submit=True):
    col1, col2 = st.columns([3,1])
    mot = col1.text_input("Le mot", placeholder="ex: vibemax")
    symbole = col2.text_input("Emoji", placeholder="🔥✨")
    
    definition = st.text_area("Définition", height=100, placeholder="Une énergie cosmique qui te fait briller en soirée")
    
    col_ia1, col_ia2 = st.columns([4,1])
    ia_suggestion = ""
    if col_ia2.button("✨ IA : rendre plus beau", type="secondary"):
        # Simulation IA (tu peux remplacer par vrai appel Claude/Grok plus tard)
        suggestions = [
            "Une explosion d'énergie pure qui te transforme en star intergalactique.",
            "Le niveau ultime de vibe qui fait trembler les pixels.",
            "Quand ton aura devient si puissante que même les écrans pleurent de joie.",
            "L'état suprême où tu brilles plus fort que mille néons."
        ]
        ia_suggestion = random.choice(suggestions)
        st.session_state.ia_temp = ia_suggestion
    
    if "ia_temp" in st.session_state:
        st.info(f"💡 Suggestion IA : {st.session_state.ia_temp}")
        if st.button("Utiliser cette version"):
            definition = st.session_state.ia_temp
            del st.session_state.ia_temp
    
    submitted = st.form_submit_button("Poster mon mot ! 🚀", use_container_width=True, type="primary")
    
    if submitted and mot.strip():
        # Classification IA automatique (simulation)
        categorie = "Poétique"
        if any(x in definition.lower() for x in ["sexe", "bite", "cul", "fuck", "merde"]):
            categorie = "Vulgaire"
        elif any(x in definition.lower() for x in ["love", "cœur", "amour", "douceur"]):
            categorie = "Romantique"
        elif any(x in definition.lower() for x in ["code", "algo", "dev", "bug", "hack"]):
            categorie = "Geek"
        
        new_word = {
            "id": len(st.session_state.words) + 1,
            "word": mot.strip(),
            "symbol": symbole.strip() or "✨",
            "definition": definition.strip(),
            "author": st.session_state.user,
            "category": categorie,
            "created": datetime.now().strftime("%d/%m %H:%M")
        }
        st.session_state.words.append(new_word)
        save_data({"users": users, "words": st.session_state.words})
        st.balloons()
        st.rerun()

# ==================== RECHERCHE + TRADUCTEUR ====================
st.subheader("Rechercher ou traduire")

col_search, col_translate = st.columns(2)
with col_search:
    search = st.text_input("🔍 Rechercher un mot ou une phrase")
with col_translate:
    phrase = st.text_input("Traduire une phrase → La Langue d'Internet")

# ==================== FEED TIKTOK ====================
filtered_words = st.session_state.words

if search:
    filtered_words = [w for w in filtered_words if search.lower() in w["word"].lower() or search.lower() in w["definition"].lower()]

if phrase:
    # Traduction magique (simulation fun)
    traduction = phrase.upper().replace(" ", " 🔥 ").replace("JE", "MOI").replace("TU", "TOI") + " MAXIMUM VIBE 💥"
    st.success(f"**Traduction** : {traduction}")

st.markdown("### Le Feed des Légendes ↓↓↓")

delete_idx = Non
