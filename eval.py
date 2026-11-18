from ingest import build_chunks
from store import get_collection, add_chunks, retrieve

TESTS = [
    {"q": "What is overfitting?", "file": "notes.pdf", "page": 12},
    # ... 20-30 of these
]

def hit_rate(col, k):
    hits = 0
    for t in TESTS:
        got = retrieve(t["q"], col, k)
        hits += any(g["file"] == t["file"] and g["page"] == t["page"] for g in got)
    return hits / len(TESTS)

for size, overlap in [(500, 50), (1000, 150), (1500, 200)]:
    col = get_collection(f"eval_{size}")
    add_chunks(build_chunks("docs/notes.pdf", "notes.pdf", size, overlap), col)
    print(size, {k: round(hit_rate(col, k), 2) for k in (1, 3, 5)})