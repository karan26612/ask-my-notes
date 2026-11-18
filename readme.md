## How it works

PDF → text per page → overlapping chunks → sentence-transformers embeddings (all-MiniLM-L6-v2)
→ ChromaDB → top-k retrieval → Gemini (answers only from retrieved context) → answer + sources

## Evaluation

I wrote 30 questions over a 15-page AI course module (Module 2: problem-solving and search),
each labelled with the page containing the answer, and measured how often the correct page
appeared in the top-k retrieved chunks.

| Chunk size / overlap | hit@1 | hit@3 | hit@5 |
|---|---|---|---|
| 500 / 50 | 0.73 | 0.97 | 1.00 |
| 1000 / 150 | 0.63 | 1.00 | 1.00 |
| 1500 / 200 | 0.67 | 0.93 | 0.97 |

**Choice:** 1000/150, because it retrieves the correct page in the top 3 for every question.
Smaller chunks rank the right page first more often but miss more at k=3.

**Out-of-scope questions:** 6 questions not covered by the document (4 on related topics such
as A* and alpha-beta pruning) were all answered with "I don't know".

**Limitations:** the test set is small and self-written, covers a single document, and measures
retrieval only, not answer quality.

## Run locally
pip install -r requirements.txt
# add GEMINI_API_KEY to a .env file
streamlit run streamlit_app.py
