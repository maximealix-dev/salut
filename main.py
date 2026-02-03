# app.py ── La Langue d'Internet ── Version unifiée, synchro + IA ── février 2026

import streamlit as st
import json
import os
import time
from datetime import datetime
import random  # pour simuler IA

DATA_FILE = "words.json"

# ────────────────────────────────────────────────
# Chargement / sauvegarde partagé
# ────────────────────────────────────────────────
def load_words():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_words(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ────────────────────────────────────────────────
# Session state initialisation
# ────────────────────────────────────────────────
if "words" not in st.session_state:
    st.session_state.words = load_words()

if "last_sync" not in st.session_state:
    st.session_state.last_sync = time.time()

if "action_delete" not in st.session_state:
    st.session_state.action_delete = None

if "action_edit" not in st.session_state:
    st.session_state.action_edit = None

# ────────────────────────────────────────────────
# Config & style TikTok-ish
# ────────────────────────────────────────────────
st.set_page_config(page_title="🌐 La Langue d'Internet", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
        .title {
            font-size: 3.8rem;
            font-weight: 900;
            background: linear-gradient(135deg, #25f4ee, #fe2c55);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 1rem 0 1.5rem;
            text-shadow: 0 0 20px rgba(37,244,238,0.5);
        }
        .card {
            background: #1a1a1a;
            border: 1px solid #25f4ee88;
            border-radius: 16px;
            padding: 1.4rem;
            margin-bottom: 1.2rem;
        }
        .symbol { font-size: 3.8rem; text-align: center; margin-bottom: 0.8rem; }
        .sync-info { color: #b0b0b0; font-size: 0.9rem; text-align: right; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌐 LA LANGUE D\'INTERNET</div>', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# Ajout de mot
# ────────────────────────────────────────────────
with st.form("add_word", clear_on_submit=True):
    st.subheader("Ajouter un mot 🔥")
    col1, col2 = st.columns([3,1])
    mot = col1.text_input("Mot", placeholder="glowvibe, zoomspark...")
    symbole = col2.text_input("Symbole", placeholder="✨ 🌊 💫")
    definition = st.text_area("Définition", height=110, placeholder="Une vibe qui claque sur le réseau...")
    synonyms = st.text_input("Synonymes (virgule séparée)")
    submitted = st.form_submit_button("Ajouter →", use_container_width=True, type="primary")

    if submitted and mot.strip() and definition.strip():
        entry = {
            "id": len(st.session_state.words) + 1,
            "word": mot.strip(),
            "symbol": symbole.strip() or "🌐",
            "definition": definition.strip(),
            "synonyms": synonyms.strip(),
            "author": "pote-anonymous",
            "createdAt": datetime.now().isoformat()
        }
        st.session_state.words.append(entry)
        save_words(st.session_state.words)
        st.success(f"**{mot.strip()}** ajouté !")
        st.rerun()

# ────────────────────────────────────────────────
# Liste des mots + actions sécurisées
# ────────────────────────────────────────────────
st.subheader(f"Mots créés ({len(st.session_state.words)})")

local_delete = None
local_edit = None

for i, w in enumerate(st.session_state.words):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_sym, col_main, col_act = st.columns([1, 5, 2])

        col_sym.markdown(f'<div class="symbol">{w["symbol"]}</div>', unsafe_allow_html=True)

        with col_main:
            if st.session_state.action_edit == i:
                new_word = st.text_input("Mot", value=w["word"], key=f"ew_{i}")
                new_def = st.text_area("Définition", value=w["definition"], height=100, key=f"ed_{i}")
                new_syn = st.text_input("Synonymes", value=w["synonyms"], key=f"es_{i}")
            else:
                st.markdown(f"**{w['word']}**")
                st.write(w["definition"])
                if w["synonyms"]:
                    st.caption(f"Synonymes : {w['synonyms']}")
                st.caption(f"Par {w['author']} • {w['createdAt'][:10]}")

        with col_act:
            if st.session_state.action_edit == i:
                if st.button("Valider", key=f"sv_{i}", type="primary"):
                    st.session_state.words[i] = {
                        **w,
                        "word": new_word,
                        "definition": new_def,
                        "synonyms": new_syn
                    }
                    save_words(st.session_state.words)
                    st.session_state.action_edit = None
                    st.rerun()
                if st.button("Annuler", key=f"cn_{i}"):
                    st.session_state.action_edit = None
                    st.rerun()
            else:
                if st.button("✏️", key=f"ed_{i}", help="Modifier"):
                    local_edit = i
                if st.button("🗑️", key=f"dl_{i}", help="Supprimer"):
                    local_delete = i

        st.markdown('</div>', unsafe_allow_html=True)

# Actions différées (clé anti-bug)
if local_delete is not None:
    del st.session_state.words[local_delete]
    save_words(st.session_state.words)
    st.rerun()

if local_edit is not None:
    st.session_state.action_edit = local_edit
    st.rerun()

# ────────────────────────────────────────────────
# Boost IA (simulation – remplace par vrai appel API si tu veux)
# ────────────────────────────────────────────────
st.subheader("Boost IA ✨")
col_ia1, col_ia2 = st.columns([4,1])
input_def = col_ia1.text_area("Définition à améliorer", height=90, placeholder="Colle une définition ici...")
if col_ia2.button("Améliorer →", type="primary"):
    if input_def.strip():
        # Simulation IA (remplace par requests.post vers Claude/Grok/OpenAI)
        short_poetic = input_def.strip()[:80] + "... (version IA poétique)"
        if len(input_def) > 40:
            short_poetic = random.choice([
                "Vibe électrique qui traverse les écrans comme un battement de cœur numérique.",
                "Éclat fugace qui fait vibrer les pixels et les âmes connectées.",
                f"{input_def[:30]}... mais en mode ultra-claque ✨"
            ])
        st.success("Version IA suggérée :")
        st.markdown(f"> **{short_poetic}**")
    else:
        st.warning("Écris une définition d'abord !")

# ────────────────────────────────────────────────
# Synchro & stats
# ────────────────────────────────────────────────
st.markdown("---")
col_sync, col_stats = st.columns([3,1])

with col_sync:
    if st.button("Rafraîchir maintenant 🔄"):
        st.session_state.words = load_words()
        st.rerun()

    st.caption(f"Dernière synchro : {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_sync))}")
    if time.time() - st.session_state.last_sync > 8:
        st.session_state.words = load_words()
        st.session_state.last_sync = time.time()
        st.rerun()

with col_stats:
    st.metric("Mots totaux", len(st.session_state.words))

# Petit footer
st.caption("Pour les potes • Synchronisé • Boost IA • 2026 vibe")
