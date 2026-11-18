from rag import ask

r, hits = ask("a question your notes answer")
print(r)
print("sources retrieved:", [(h["file"], h["page"]) for h in hits])

r, hits = ask("What is a state space")
print(r)