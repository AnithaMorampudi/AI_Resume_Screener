# placeholder for embedding similarity, ready for SBERT upgrade later
def compute_similarity(a, b):
    return len(set(a.lower().split()) & set(b.lower().split())) / max(len(a.split()), 1)
