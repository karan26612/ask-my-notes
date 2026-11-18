from pypdf import PdfReader

def chunk_text(text, size=1000, overlap=150):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

def build_chunks(path, name, size=1000, overlap=150):
    out = []
    for page_no, page in enumerate(PdfReader(path).pages, start=1):
        for c in chunk_text(page.extract_text() or "", size, overlap):
            if len(c.strip()) > 50:
                out.append({"text": c, "file": name, "page": page_no})
    return out

if __name__ == "__main__":
    chunks = build_chunks("docs/notes.pdf", "notes.pdf")
    print("chunks:", len(chunks))
    print("pages:", sorted({c["page"] for c in chunks})[:5])
    print("min/max length:", min(len(c["text"]) for c in chunks), max(len(c["text"]) for c in chunks))
    print("---\n", chunks[3]["text"][:300])