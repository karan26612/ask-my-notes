from ingest import build_chunks
from store import client, get_collection, add_chunks, retrieve

PDF, NAME = "docs/notes.pdf", "notes.pdf"   # must match your file in docs/

TESTS = [
    {"q": "What is the first thing an agent does when it begins solving a problem?", "page": 1},
    {"q": "What are the three phases of the simple problem-solving agent design?", "page": 1},
    {"q": "How does the transition model describe what an action does?", "page": 2},
    {"q": "In a state-space graph, what do the nodes and the links represent?", "page": 2},
    {"q": "Why do we leave out details like the weather or the radio when describing a state?", "page": 3},
    {"q": "What makes an abstraction valid, and what makes it useful?", "page": 3},
    {"q": "How many states does the two-square vacuum world have, and what is the formula for n locations?", "page": 3},
    {"q": "Which actions are available in the vacuum world, and when do they have no effect?", "page": 4},
    {"q": "What fraction of starting configurations of the 8-puzzle can reach a given goal?", "page": 4},
    {"q": "How many reachable states does the 8-puzzle have?", "page": 5},
    {"q": "Which complexity class do sliding-block puzzles belong to?", "page": 5},
    {"q": "What is the difference between incremental and complete-state formulations of the 8-queens problem?", "page": 5},
    {"q": "By how much does the improved 8-queens formulation shrink the state space?", "page": 6},
    {"q": "Who proposed the problem of reaching any positive integer from 4 using factorial, square root and floor?", "page": 6},
    {"q": "What extra information must a state keep in a touring problem?", "page": 6},
    {"q": "How is a search tree different from a state space?", "page": 7},
    {"q": "What is the explored set used for in graph search?", "page": 8},
    {"q": "What four pieces of information does each search-tree node store?", "page": 9},
    {"q": "Which data structure holds the frontier, and what operations does it support?", "page": 9},
    {"q": "What are the four criteria used to evaluate a search algorithm?", "page": 10},
    {"q": "Why does breadth-first search use a first-in-first-out queue?", "page": 10},
    {"q": "What is the worst-case time complexity of breadth-first search?", "page": 11},
    {"q": "Why does depth-first search need so little memory?", "page": 11},
    {"q": "What problems can depth-first search run into, such as loops?", "page": 12},
    {"q": "How does iterative deepening search find the right depth limit?", "page": 12},
    {"q": "For branching factor 10 and depth 5, how many nodes do IDS and BFS generate?", "page": 13},
    {"q": "What are the two kinds of failure a depth-limited search can return?", "page": 14},
    {"q": "Which data structure orders the frontier in uniform-cost search?", "page": 14},
    {"q": "What is the cost of the best route from Sibiu to Bucharest in the uniform-cost example?", "page": 15},
    {"q": "When does a bidirectional search stop, and what is its time complexity?", "page": 15},
]

UNANSWERABLE = [
    "What is the capital of Australia?",
    "Who won the 2018 FIFA World Cup?",
    "How does the A* algorithm use a heuristic function?",
    "What is alpha-beta pruning in game playing?",
    "How does greedy best-first search pick the next node to expand?",
    "What is a constraint satisfaction problem?",
]


def hit_rate(col, k):
    hits = 0
    for t in TESTS:
        got = retrieve(t["q"], col, k)
        hits += any(g["file"] == NAME and g["page"] == t["page"] for g in got)
    return hits / len(TESTS)


def fresh_collection(name):
    try:
        client.delete_collection(name)
    except Exception:
        pass
    return get_collection(name)


if __name__ == "__main__":
    configs = [(500, 50), (1000, 150), (1500, 200)]
    cols = {}

    print(f"{len(TESTS)} test questions\n")
    print("chunk size | overlap | hit@1  hit@3  hit@5")
    for size, overlap in configs:
        col = fresh_collection(f"eval_{size}")
        add_chunks(build_chunks(PDF, NAME, size, overlap), col)
        cols[size] = col
        r = {k: round(hit_rate(col, k), 2) for k in (1, 3, 5)}
        print(f"{size:>10} | {overlap:>7} | {r[1]:<6} {r[3]:<6} {r[5]}")

    best = max(cols, key=lambda s: hit_rate(cols[s], 3))
    print(f"\nBest chunk size at k=3: {best}")
    print("\nMisses at k=3:")
    for t in TESTS:
        got = retrieve(t["q"], cols[best], 3)
        if not any(g["page"] == t["page"] for g in got):
            print(f"- {t['q']} (expected p.{t['page']}) -> got pages {[g['page'] for g in got]}")