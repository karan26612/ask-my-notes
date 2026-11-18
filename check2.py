from ingest import build_chunks
from store import get_collection, add_chunks, retrieve, model

col = get_collection("test")
chunks = build_chunks("docs/notes.pdf", "notes.pdf")
add_chunks(chunks, col)

print("stored:", col.count(), "expected:", len(chunks))
print("embedding size:", len(model.encode("hello")))

for q in ["What is a state space?", "banana pizza recipe"]:
    print("\nQ:", q)
    for h in retrieve(q, col, k=3):
        print(" ", h["file"], "p.", h["page"], "|", h["text"][:100].replace("\n", " "))