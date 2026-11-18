from rag import ask
from eval import UNANSWERABLE

refused = 0
for q in UNANSWERABLE:
    r, _ = ask(q)
    print(q, "->", r["answer"][:100])
    a = r["answer"].lower()
    refused += ("don't know" in a) or ("do not know" in a)
print(f"\nCorrect refusals: {refused}/{len(UNANSWERABLE)}")