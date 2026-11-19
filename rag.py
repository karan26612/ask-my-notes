try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import json
import os
from google import genai
from store import get_collection, retrieve

MODEL = "gemini-3.5-flash-lite"   # use the model name that worked in check0.py

PROMPT = """Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.
Return JSON: {{"answer": "...", "sources": [{{"file": "...", "page": 1}}]}}

Context:
{context}

Question: {question}"""

_client = None


def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]   # Streamlit Cloud secret
    except Exception:
        return None


def get_client():
    global _client
    if _client is None:
        key = get_api_key()
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not configured on the server.")
        _client = genai.Client(api_key=key)
    return _client


def ask(question, k=4, col=None):
    col = col or get_collection()
    hits = retrieve(question, col, k)
    context = "\n\n".join(f"[{h['file']} p.{h['page']}] {h['text']}" for h in hits)
    r = get_client().models.generate_content(
        model=MODEL,
        contents=PROMPT.format(context=context, question=question),
        config={"response_mime_type": "application/json"},
    )
    return json.loads(r.text), hits