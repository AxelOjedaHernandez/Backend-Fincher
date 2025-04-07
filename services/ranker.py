from sentence_transformers import SentenceTransformer, util

# Cargar modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_compounds(compounds: list, query: str, top_k: int = 100) -> list:
    if not compounds or not query:
        return compounds[:top_k]

    # Embeddings de compuestos (nombre + fórmula)
    texts = [f"{c['nombre']} {c['formula']}" for c in compounds]
    compound_embeddings = model.encode(texts, convert_to_tensor=True)

    # Embedding de la query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Calcular similitud coseno
    similarities = util.cos_sim(query_embedding, compound_embeddings)[0]

    # Asociar score a cada compuesto
    for i, score in enumerate(similarities):
        compounds[i]["score"] = score.item()

    # Ordenar y limitar
    ranked = sorted(compounds, key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]

