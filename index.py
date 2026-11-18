from ingest import build_chunks
from store import get_collection, add_chunks

col = get_collection()   # defaults to "notes"
chunks = build_chunks("docs/notes.pdf", "notes.pdf")
add_chunks(chunks, col)
print("indexed:", col.count())