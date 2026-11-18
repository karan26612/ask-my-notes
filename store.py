import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="db")

def get_collection(name="notes"):
    return client.get_or_create_collection(name, metadata={"hnsw:space": "cosine"})

def add_chunks(chunks, col):
    col.upsert(
        ids=[f"{c['file']}-{i}" for i, c in enumerate(chunks)],
        documents=[c["text"] for c in chunks],
        embeddings=model.encode([c["text"] for c in chunks]).tolist(),
        metadatas=[{"file": c["file"], "page": c["page"]} for c in chunks],
    )

def retrieve(question, col, k=4):
    res = col.query(query_embeddings=model.encode([question]).tolist(), n_results=k)
    return [{"text": d, **m} for d, m in zip(res["documents"][0], res["metadatas"][0])]