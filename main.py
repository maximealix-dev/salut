# app.py ── LA LANGUE D'INTERNET ── Version finale complète ── février 2026

import streamlit as st
import json
import os
import time
from datetime import datetime
import random

# =============================================================================
# CONFIGURATION GLOBALE
# =============================================================================
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
users = data.get("users", {})
words = data.get("words", [])

# =============================================================================
# SESSION STATE
# =============================================================================
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

# =============================================================================
# STYLE TIKTOK / MODERNE
# =============================================================================
st.set_page_config(page_title="🌐 La Langue d'Internet", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;600;700;900&display=swap');
    
    .stApp { background: #000; color: white; }
    .titre { 
        font-family: 'Bebas Neue', sans-serif;
        font-size: 5rem; 
        background: linear-gradient(90deg, #fe2c55, #25f4ee, #a033ff, #fe2c55);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1.5rem 0 2rem;
        animation: gradient 8s ease infinite;
    }
    @keyframes gradient { 0% {background-position:0% 50%} 50% {background-position:100% 50%} 100% {background-position:0% 50%} }
    
    .card {
        background: rgba(20,20,40,0.92);
        border-radius: 20px;
        padding: 1.8rem;
        margin: 1.2rem auto;
        max-width: 680px;
        border: 1px solid #25f4ee44;
        box-shadow: 0 12px 40px rgba(37,244,238,0.18);
        backdrop-filter: blur(12px);
    }
    .emoji-big { font-size: 5.5rem; text-align: center; margin: 0.5rem 0; filter: drop-shadow(0 0 15px #00f2ea); }
    .mot-titre { font-size: 2.8rem; font-weight: 900; text-align: center; color: #25f4ee; margin: 0.4rem 0; }
    .definition { font-size: 1.25rem; text-align: center; line-height: 1.6; color: #e0e0ff; margin: 1rem 0; }
    .tag { background: #fe2c55; color: white; padding: 0.35rem 0.9rem; border-radius: 30px; font-size: 0.85rem; margin: 0.3rem 0.2rem; display: inline-block; }
    .author { text-align: center; color: #aaa; font-size: 0.95rem; margin-top: 1rem; }
    .btn { border-radius: 50px !important; font-weight: bold !important; }
    .btn-primary { background: linear-gradient(90deg, #fe2c55, #a033ff) !important; }
    .btn-ia { background: linear-gradient(90deg, #833ab4, #25f4ee) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">🌐 LA LANGUE D\'INTERNET</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ccc; font-size:1.3rem; margin-bottom:2rem;'>Crée, partage et traduis la langue du futur avec tes potes 🔥</p>", unsafe_allow_html=True)

# =============================================================================
# CONNEXION / INSCRIPTION
# =============================================================================
if not st.session_state.user:
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        st.subheader("Connexion")
        login_user = st.text_input("Pseudo", key="l_user")
        login_pass = st.text_input("Mot de passe", type="password", key="l_pass")
        if st.button("Se connecter", type="primary", use_container_width=True):
            if login_user in users and users[login_user]["password"] == login_pass:
                st.session_state.user = login_user
                st.success(f"Bienvenue {login_user} ! 🌟")
                st.rerun()
            else:
                st.error("Pseudo ou mot de passe incorrect")
    
    with tab2:
        st.subheader("Inscription")
        new_user = st.text_input("Pseudo", key="n_user")
        new_pass = st.text_input("Mot de passe", type="password", key="n_pass")
        if st.button("Créer mon compte", type="primary", use_container_width=True):
            if new_user in users:
                st.error("Ce pseudo est déjà pris")
            elif len(new_user) < 3:
                st.error("Pseudo trop court (≥ 3 caractères)")
            else:
                users[new_user] = {"password": new_pass}
                save_data({"users": users, "words": st.session_state.words})
                st.success("Compte créé ! Connecte-toi maintenant")
                st.rerun()
    st.stop()

# =============================================================================
# AJOUT DE MOT + IA
# =============================================================================
st.subheader("Créer un nouveau mot")

with st.form("add_word_form", clear_on_submit=True):
    col1, col2 = st.columns([3,1])
    mot = col1.text_input("Le mot", placeholder="vibemax, glowvibe, zoomspark...")
    symbole = col2.text_input("Emoji", placeholder="🔥 ✨ 💫")

    definition = st.text_area("Définition", height=110,
                             placeholder="Une énergie cosmique qui te fait briller en soirée...")

    col_ia1, col_ia2 = st.columns([4,1])
    if col_ia2.button("✨ IA : rendre plus beau", type="secondary"):
        suggestions = [
            "Une vibe qui explose les pixels et fait danser les cœurs.",
            "État ultime où tu deviens la star de tous les écrans.",
            "L'énergie pure qui transforme la nuit en feu d'artifice digital.",
            "Quand ton aura devient si forte que même les stories tremblent."
        ]
        st.session_state.ia_suggest = random.choice(suggestions)

    if "ia_suggest" in st.session_state:
        st.info(f"**Suggestion IA** : {st.session_state.ia_suggest}")
        if st.button("Utiliser cette version"):
            definition = st.session_state.ia_suggest
            del st.session_state.ia_suggest

    if st.form_submit_button("Poster mon mot ! 🚀", type="primary", use_container_width=True):
        if mot.strip() and definition.strip():
            cat = "Poétique"
            lower_def = definition.lower()
            if any(w in lower_def for w in ["sexe", "bite", "cul", "fuck", "merde", "pute"]):
                cat = "Vulgaire"
            elif any(w in lower_def for w in ["love", "cœur", "amour", "douceur", "tendre"]):
                cat = "Romantique"
            elif any(w in lower_def for w in ["code", "bug", "hack", "python", "dev", "algo"]):
                cat = "Geek"

            nouveau = {
                "id": len(st.session_state.words) + 1,
                "word": mot.strip(),
                "symbol": symbole.strip() or random.choice(["🔥","✨","💫","🦄","😎"]),
                "definition": definition.strip(),
                "author": st.session_state.user,
                "category": cat,
                "created": datetime.now().strftime("%d/%m %H:%M")
            }
            st.session_state.words.append(nouveau)
            save_data({"users": users, "words": st.session_state.words})
            st.balloons()
            st.success(f"Posté ! **{mot.strip()}** est dans le feed 🔥")
            st.rerun()

# =============================================================================
# RECHERCHE + TRADUCTEUR
# =============================================================================
st.subheader("Rechercher ou traduire")
col_r, col_t = st.columns(2)

with col_r:
    recherche = st.text_input("🔍 Chercher un mot ou une phrase")

with col_t:
    phrase_a_traduire = st.text_input("Traduire une phrase → La Langue d'Internet")

if phrase_a_traduire:
    # Traduction fun et créative
    mots = phrase_a_traduire.split()
    trad = " ".join([f"{m.upper()}💥" if random.random() > 0.5 else f"{m}✨" for m in mots])
    trad += random.choice([" 🔥 MAX VIBE", " 🌌 ULTRA GLOW", " 💫 COSMIC FLOW"])
    st.success(f"**Traduction** : {trad}")

# =============================================================================
# FEED TIKTOK (cartes verticales)
# =============================================================================
filtered = st.session_state.words
if recherche:
    recherche_lower = recherche.lower()
    filtered = [w for w in filtered if recherche_lower in w["word"].lower() or recherche_lower in w["definition"].lower()]

st.markdown("### Le Feed des Légendes ↓↓↓")

delete_idx = None
edit_idx = None

for i, w in enumerate(filtered[::-1]):  # récent en haut
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown(f'<div class="emoji-big">{w["symbol"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mot-titre">{w["word"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="definition">{w["definition"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2,1])
        col1.markdown(f'<span class="tag">{w["category"]}</span>', unsafe_allow_html=True)
        col2.markdown(f'<div class="author">Par {w["author"]} • {w["created"]}</div>', unsafe_allow_html=True)
        
        if w["author"] == st.session_state.user:
            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("✏️ Modifier", key=f"edit_{i}"):
                edit_idx = len(filtered) - 1 - i
            if col_btn2.button("🗑️ Supprimer", key=f"del_{i}", type="primary"):
                delete_idx = len(filtered) - 1 - i
        
        st.markdown('</div>', unsafe_allow_html=True)

# Actions sécurisées
if delete_idx is not None:
    del st.session_state.words[delete_idx]
    save_data({"users": users, "words": st.session_state.words})
    st.rerun()

if edit_idx is not None:
    st.session_state.edit_idx = edit_idx
    st.rerun()

# =============================================================================
# SYNCHRONISATION AUTO + BOUTON
# =============================================================================
if time.time() - st.session_state.last_sync > 8:
    new_data = load_data()
    st.session_state.words = new_data.get("words", [])
    st.session_state.last_sync = time.time()
    st.rerun()

col_sync, col_user = st.columns([3,1])
with col_sync:
    if st.button("Rafraîchir maintenant 🔄"):
        st.session_state.words = load_data().get("words", [])
        st.session_state.last_sync = time.time()
        st.rerun()
with col_user:
    st.caption(f"Connecté : {st.session_state.user}")

st.caption(f"{len(st.session_state.words)} mots dans la langue • Mis à jour à {time.strftime('%H:%M:%S')}")
