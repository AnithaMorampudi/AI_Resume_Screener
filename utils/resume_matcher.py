from sentence_transformers import SentenceTransformer, util
import numpy as np
import re

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_keywords(text):
    """Extract relevant keywords from JD text."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#]', ' ', text)
    words = text.split()
    stop_words = set([
        'the','and','for','with','that','this','are','was','were','to','of','in','on','as','at','by','be','an','it','or','from'
    ])
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    # Keep unique terms
    return list(set(keywords))

def compare_keywords_semantic(resume_text, jd_text, threshold_high=0.7, threshold_low=0.4):
    jd_keywords = extract_keywords(jd_text)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_embs = model.encode(jd_keywords, convert_to_tensor=True)

    similarities = util.cos_sim(jd_embs, resume_emb)

    results = []
    for idx, kw in enumerate(jd_keywords):
        sim = float(similarities[idx].max())
        if sim >= threshold_high:
            status = "✅ Strong Match"
        elif sim >= threshold_low:
            status = "⚠️ Partial Match"
        else:
            status = "❌ Missing"
        results.append((kw, round(sim*100, 1), status))
    
    return sorted(results, key=lambda x: x[1], reverse=True)
