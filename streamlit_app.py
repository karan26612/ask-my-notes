from dotenv import load_dotenv
load_dotenv()
import os, tempfile
import streamlit as st
from ingest import build_chunks
from store import get_collection, add_chunks
from rag import ask

st.set_page_config(page_title="Ask My Notes", page_icon="📚")
st.title("📚 Ask My Notes")
st.caption("Upload PDFs and ask questions answered from them, with page citations.")

col = get_collection()

with st.sidebar:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Index documents") and files:
        for f in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(f.read())
            add_chunks(build_chunks(tmp.name, f.name), col)
            os.unlink(tmp.name)
        st.success(f"Indexed. Total chunks: {col.count()}")

q = st.text_input("Your question", placeholder="e.g. What is a state space?")
if st.button("Ask", type="primary") and q.strip():
    result, hits = ask(q, col=col)
    st.write(result["answer"])
    with st.expander("Sources"):
        for h in hits:
            st.markdown(f"**{h['file']}, page {h['page']}**")
            st.caption(h["text"][:300] + "...")