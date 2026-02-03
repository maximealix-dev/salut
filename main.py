# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json
import os
from datetime import datetime
from passlib.context import CryptContext  # pip install passlib[bcrypt]

app = FastAPI(title="La Langue d'Internet - Potes Edition")

# Sécurité mots de passe (pas critique pour potes, mais mieux que rien)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dossier data
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
USERS_FILE = os.path.join(DATA_DIR, "users.json")
WORDS_FILE = os.path.join(DATA_DIR, "words.json")

def load_data(file_path, default):
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users_db = load_data(USERS_FILE, [])
words_db = load_data(WORDS_FILE, [])

# Modèles
class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class WordCreate(BaseModel):
    word: str
    symbol: Optional[str] = "🌐"
    definition: str
    synonyms: Optional[str] = ""
    category: Optional[str] = "Général"

# Routes API simples
@app.post("/api/register")
def register(data: Register):
    if any(u["username"] == data.username for u in users_db):
        raise HTTPException(400, "Pseudo déjà pris entre potes")
    hashed = pwd_context.hash(data.password)
    users_db.append({"username": data.username, "password": hashed})
    save_data(USERS_FILE, users_db)
    return {"ok": True, "message": "Compte créé, connecte-toi maintenant"}

@app.post("/api/login")
def login(data: Login):
    user = next((u for u in users_db if u["username"] == data.username), None)
    if not user or not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(401, "Mauvais pseudo ou mdp")
    return {"ok": True, "username": data.username}

@app.get("/api/words")
def get_words():
    return words_db

@app.post("/api/words")
def add_word(word: WordCreate):
    # Pour l'instant pas d'auth forcée → anonymous ou via header plus tard
    new_word = {
        "id": len(words_db) + 1,
        "word": word.word.strip(),
        "symbol": word.symbol.strip(),
        "definition": word.definition.strip(),
        "synonyms": word.synonyms.strip(),
        "category": word.category,
        "author": "pote-anonymous",  # ← à remplacer par current user plus tard
        "createdAt": datetime.utcnow().isoformat()
    }
    words_db.append(new_word)
    save_data(WORDS_FILE, words_db)
    return new_word

# Servir ton HTML magique
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("la-langue-internet.html", encoding="utf-8") as f:
        return f.read()

# Optionnel : servir pixel arts persistants plus tard
app.mount("/static", StaticFiles(directory="static"), name="static")