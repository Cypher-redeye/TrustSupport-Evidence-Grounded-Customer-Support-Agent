import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

def main():
    data_dir = Path("data/processed")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # 1. Load Evidence Dataset
    print("Loading evidence items...")
    evidence = []
    with open(data_dir / "intent_evidence.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            evidence.append(json.loads(line))
            
    # Deterministic sorting
    evidence.sort(key=lambda x: x["evidence_id"])
    print(f"Total evidence items: {len(evidence)}")
    
    texts = [item["customer_text"] for item in evidence]
    
    # 2. Embed
    print("Embedding texts...")
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    embeds = encoder.encode(texts, show_progress_bar=True)
    
    # 3. L2 Normalize
    print("L2 normalizing embeddings...")
    faiss.normalize_L2(embeds)
    
    # 4. Save Embeddings
    embeds_path = models_dir / "train_evidence_embeddings.npy"
    np.save(embeds_path, embeds)
    print(f"Saved embeddings to {embeds_path}")
    
    # 5. Build FAISS Index
    print("Building FAISS IndexFlatIP...")
    dim = embeds.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeds)
    
    index_path = models_dir / "evidence.index"
    faiss.write_index(index, str(index_path))
    print(f"Saved index to {index_path}")
    
    # 6. Save Metadata
    # Remove customer_text since it's embedded, save everything else to reduce file size
    for item in evidence:
        del item["customer_text"]
        
    metadata_path = models_dir / "evidence_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(evidence, f)
    print(f"Saved metadata to {metadata_path}")
    
    print("Index building complete.")

if __name__ == "__main__":
    main()
