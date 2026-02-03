# app.py ── LA LANGUE D'INTERNET ── Version corrigée complète ── février 2026

import streamlit as st
import json
import os
import time
from datetime import datetime
import random

# =============================================================================
# FICHIER DE DONNÉES
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

# =============================================================================
# STYLE TIKTOK / MODERNE
# =============================================================================
st.set_page_config(page_title="🌐 La Langue d'Internet", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    .titre { 
        font-size: 4.5rem; 
        font-weight: 900;
        background: linear-gradient(90deg, #fe2c55, #25f4ee, #a033ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1.5rem 0 2rem;
        text-shadow: 0 0 20px rgba(254,44,85,0.6);
    }
    .card {
        background: rgba(20,20,40,0.92);
        border-radius: 20px;
        padding: 1.6rem;
        margin: 1.2rem auto;
        max-width: 700px;
        border: 1px solid #25f4ee55;
        box-shadow: 0 10px 30px rgba(37,244,238,0.2);
        backdrop-filter: blur(8px);
    }
    .emoji-big { font-size: 5rem; text-align: center; margin: 0.5rem 0; }
    .mot { font-size: 2.6rem; font-weight: 900; text-align: center; color: #25f4ee; }
    .def { font-size: 1.2rem; text-align: center; color: #e0e0ff; margin: 1rem 0; }
    .tag { background: #fe2c55; color: white; padding: 0.4rem 1rem; border-radius: 30px; font-size: 0.9rem; margin: 0.3rem; display: inline-block; }
    .author { text-align: center; color: #bbb; font-size: 0.95rem; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">🌐 LA LANGUE D\'INTERNET</div>', unsafe_allow_html=True)

# =============================================================================
# CONNEXION / INSCRIPTION
# =============================================================================
if not st.session_state.user:
    tab_conn, tab_insc = st.tabs(["Connexion", "Inscription"])

    with tab_conn:
        st.subheader("Connexion")
        l_user = st.text_input("Pseudo", key="login_user")
        l_pass = st.text_input("Mot de passe", type="password", key="login_pass")
        if st.button("Se connecter", type="primary", use_container_width=True):
            if l_user in users and users[l_user]["password"] == l_pass:
                st.session_state.user = l_user
                st.success(f"Bienvenue {l_user} ! 🌟")
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    with tab_insc:
        st.subheader("Inscription")
        n_user = st.text_input("Pseudo", key="new_user")
        n_pass = st.text_input("Mot de passe", type="password", key="new_pass")
        if st.button("Créer compte", type="primary", use_container_width=True):
            if n_user in users:
                st.error("Pseudo déjà utilisé")
            elif len(n_user) < 3:
                st.error("Pseudo trop court (min 3 caractères)")
            else:
                users[n_user] = {"password": n_pass}
                save_data({"users": users, "words": st.session_state.words})
                st.success("Compte créé ! Connecte-toi")
                st.rerun()
    st.stop()

# =============================================================================
# AJOUT DE MOT + IA
# =============================================================================
st.subheader("Créer un nouveau mot")

with st.form("add_word_form", clear_on_submit=True):
    col_mot, col_emo = st.columns([3, 1])
    mot = col_mot.text_input("Le mot", placeholder="vibemax, glowvibe...")
    symbole = col_emo.text_input("Emoji", placeholder="🔥 ✨")

    definition = st.text_area("Définition", height=110,
                             placeholder="Une énergie qui fait briller toute la soirée...")

    # Bouton IA (submit pour déclencher suggestion)
    if st.form_submit_button("✨ IA : rendre plus beau", help="Génère une version stylée"):
        # Simulation IA (tu peux remplacer par vrai appel API)
        suggestions = [
            "Une vibe qui explose les écrans et fait danser les cœurs.",
            "État ultime où tu deviens la star absolue du feed.",
            "L'énergie pure qui transforme la nuit en feu digital."
        ]
        st.session_state.ia_suggest = random.choice(suggestions)

    if "ia_suggest" in st.session_state:
        st.info(f"**IA suggère** : {st.session_state.ia_suggest}")
        if st.button("Utiliser cette version"):
            definition = st.session_state.ia_suggest
            del st.session_state.ia_suggest

    # Bouton principal d'enregistrement (OBLIGATOIRE dans le form)
    if st.form_submit_button("Poster mon mot ! 🚀", type="primary", use_container_width=True):
        if mot.strip() and definition.strip():
            cat = "Poétique"
            lower = definition.lower()
            if any(w in lower for w in ["sexe", "bite", "cul", "fuck", "merde"]):
                cat = "Vulgaire"
            elif any(w in lower for w in ["love", "amour", "cœur"]):
                cat = "Romantique"
            elif any(w in lower for w in ["code", "bug", "python", "hack"]):
                cat = "Geek"

            nouveau = {
                "word": mot.strip(),
                "symbol": symbole.strip() or "🌟",
                "definition": definition.strip(),
                "author": st.session_state.user,
                "category": cat,
                "created": datetime.now().strftime("%d/%m %H:%M")
            }
            st.session_state.words.append(nouveau)
            save_data({"users": users, "words": st.session_state.words})
            st.balloons()
            st.success(f"Posté ! **{mot.strip()}** est live 🔥")
            st.rerun()

# =============================================================================
# RECHERCHE + TRADUCTEUR
# =============================================================================
st.subheader("Rechercher ou traduire")
col_r, col_tr = st.columns(2)
recherche = col_r.text_input("🔍 Chercher un mot / phrase")
phrase = col_tr.text_input("Traduire une phrase → Langue Internet")

if phrase:
    # Traduction fun
    trad = phrase.upper().replace(" ", " 💥 ").replace("JE", "MOI").replace("TU", "TOI") + " VIBE MAX 🔥"
    st.success(f"**Traduction** : {trad}")

# =============================================================================
# FEED (cartes TikTok)
# =============================================================================
filtered = st.session_state.words
if recherche:
    lower = recherche.lower()
    filtered = [w for w in filtered if lower in w["word"].lower() or lower in w["definition"].lower()]

st.markdown("### Feed des potes ↓↓↓")

delete_idx = None
edit_idx = None

for i, w in enumerate(filtered[::-1]):  # récent en haut
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown(f'<div class="emoji-big">{w["symbol"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mot">{w["word"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="def">{w["definition"]}</div>', unsafe_allow_html=True)
        
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

# Actions après boucle
if delete_idx is not None:
    del st.session_state.words[delete_idx]
    save_data({"users": users, "words": st.session_state.words})
    st.rerun()

if edit_idx is not None:
    st.session_state.edit_idx = edit_idx
    st.rerun()

# =============================================================================
# SYNCHRO AUTO
# =============================================================================
if time.time() - st.session_state.last_sync > 8:
    new_data = load_data()
    st.session_state.words = new_data.get("words", [])
    st.session_state.last_sync = time.time()
    st.rerun()

st.caption(f"Connecté : {st.session_state.user} • {len(st.session_state.words)} mots • Synchro auto 8s")
