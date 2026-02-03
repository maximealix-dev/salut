# app.py ── La Langue d'Internet ── Version collégiens ── février 2026

import streamlit as st
import json
import os
import time
from datetime import datetime

DATA_FILE = "words.json"

# ─── Chargement / sauvegarde ───
def load_words():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_words(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Initialisation ───
if "words" not in st.session_state:
    st.session_state.words = load_words()

if "last_sync" not in st.session_state:
    st.session_state.last_sync = time.time()

if "action_delete" not in st.session_state:
    st.session_state.action_delete = None

# ─── Page config & couleurs sympas pour collégiens ───
st.set_page_config(
    page_title="La Langue d'Internet",
    page_icon="🌈",
    layout="wide"
)

st.markdown("""
    <style>
        .titre {
            font-size: 3.2rem;
            color: #ff6bcb;
            text-align: center;
            margin: 1rem 0;
            font-family: 'Comic Sans MS', cursive;
        }
        .carte {
            background: #f0f8ff;
            border: 3px solid #77dd77;
            border-radius: 16px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .symbole { font-size: 3.5rem; text-align: center; margin-bottom: 0.6rem; }
        .bouton-suppr { background: #ff6961; color: white; }
        .bouton-suppr:hover { background: #ff4d4d; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titre">🌈 La Langue d\'Internet 🌈</div>', unsafe_allow_html=True)
st.markdown("**Invente des mots trop stylés avec tes potes !** 😎", unsafe_allow_html=True)

# ─── Ajouter un mot ───
st.subheader("Ajouter un mot trop cool")
with st.form("ajout", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    mot = col1.text_input("Le mot inventé", placeholder="ex: kawaiizor")
    symbole = col2.text_input("Emoji", placeholder="🐱✨")

    definition = st.text_area("Ça veut dire quoi ?", height=100, placeholder="C'est quand t'es super content et que tu sautes partout !")
    submitted = st.form_submit_button("Envoyer mon mot ! 🚀", use_container_width=True)

    if submitted and mot.strip() and definition.strip():
        nouveau = {
            "id": len(st.session_state.words) + 1,
            "word": mot.strip(),
            "symbol": symbole.strip() or "🌟",
            "definition": definition.strip(),
            "created": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        st.session_state.words.append(nouveau)
        save_words(st.session_state.words)
        st.balloons()
        st.success(f"Trop bien ! **{mot.strip()}** est ajouté ! 🎉")

# ─── Liste des mots ───
st.subheader(f"Mots de la classe ({len(st.session_state.words)})")

local_delete = None

for i, mot in enumerate(st.session_state.words):
    with st.container():
        st.markdown('<div class="carte">', unsafe_allow_html=True)

        col_emo, col_texte, col_btn = st.columns([1, 5, 1])

        col_emo.markdown(f'<div class="symbole">{mot["symbol"]}</div>', unsafe_allow_html=True)

        with col_texte:
            st.markdown(f"**{mot['word']}**")
            st.write(mot["definition"])
            st.caption(f"Ajouté le {mot['created']}")

        with col_btn:
            if st.button("🗑️", key=f"suppr_{i}_{mot['id']}", help="Supprimer ce mot", type="primary"):
                local_delete = i

        st.markdown('</div>', unsafe_allow_html=True)

# Suppression différée (anti-bug)
if local_delete is not None:
    del st.session_state.words[local_delete]
    save_words(st.session_state.words)
    st.rerun()

# ─── Rafraîchissement automatique + bouton manuel ───
if time.time() - st.session_state.last_sync > 10:
    st.session_state.words = load_words()
    st.session_state.last_sync = time.time()
    st.rerun()

col1, col2 = st.columns([3,1])
with col1:
    st.caption(f"Dernière mise à jour : {time.strftime('%H:%M:%S')}")
with col2:
    if st.button("Rafraîchir maintenant 🔄"):
        st.session_state.words = load_words()
        st.session_state.last_sync = time.time()
        st.rerun()

st.markdown("---")
st.caption("Partagé avec toute la classe • Tous les mots sont visibles par tout le monde")
