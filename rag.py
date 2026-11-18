from dotenv import load_dotenv
load_dotenv()
import json, os
from google import genai
from store import get_collection, retrieve

gclient = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash-lite"   # use the same Gemini model name as in EcoSpark

PROMPT = """Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.
Return JSON: {{"answer": "...", "sources": [{{"file": "...", "page": 1}}]}}

Context:
{context}

Question: {question}"""

def ask(question, k=4, col=None):
    col = col or get_collection()
    hits = retrieve(question, col, k)
    context = "\n\n".join(f"[{h['file']} p.{h['page']}] {h['text']}" for h in hits)
    r = gclient.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(context=context, question=question),
        config={"response_mime_type": "application/json"},
    )
    return json.loads(r.text), hits