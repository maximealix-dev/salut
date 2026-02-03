# langue_streamlit.py

import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "words.json"

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "words" not in st.session_state:
    st.session_state.words = load()

if "action_delete" not in st.session_state:
    st.session_state.action_delete = None

st.title("🌐 LA LANGUE D'INTERNET")
st.markdown("Créez et partagez votre langue entre potes ! ✨")

# Ajout
with st.form("ajout"):
    mot = st.text_input("Mot")
    symbole = st.text_input("Symbole", "🌐")
    defi = st.text_area("Définition")
    syn = st.text_input("Synonymes")
    if st.form_submit_button("Ajouter"):
        if mot and defi:
            st.session_state.words.append({
                "word": mot,
                "symbol": symbole,
                "definition": defi,
                "synonyms": syn,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save(st.session_state.words)
            st.success("Ajouté !")

# Liste
delete_idx = None
for i, w in enumerate(st.session_state.words):
    with st.container(border=True):
        st.markdown(f"**{w['symbol']} {w['word']}**")
        st.write(w["definition"])
        if w["synonyms"]:
            st.caption(f"Synonymes : {w['synonyms']}")
        if st.button("🗑️ Supprimer", key=f"del_{i}"):
            delete_idx = i

if delete_idx is not None:
    del st.session_state.words[delete_idx]
    save(st.session_state.words)
    st.rerun()

st.caption(f"{len(st.session_state.words)} mots")
