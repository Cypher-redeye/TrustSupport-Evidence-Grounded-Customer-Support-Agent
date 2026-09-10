import json
import numpy as np
from pathlib import Path
from src.config import settings
from sklearn.cluster import KMeans

def analyze_unmapped():
    embed_file = Path(settings.processed_data_dir) / "intent_embeddings.npz"
    cache = np.load(embed_file)
    embeddings = cache['embeddings']
    request_ids = cache['request_ids']
    
    sample_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    requests = {}
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            req = json.loads(line)
            requests[req['request_id']] = req

    model = KMeans(n_clusters=10, random_state=settings.random_seed, n_init=10)
    labels = model.fit_predict(embeddings)
    
    unmapped_counts = {}
    examples = []
    
    for i in range(len(request_ids)):
        c_id = labels[i]
        # Mapped clusters: 0, 1, 2, 3, 4, 5, 6, 7, 8
        if c_id == 9:
            unmapped_counts[c_id] = unmapped_counts.get(c_id, 0) + 1
            if len(examples) < 20:
                examples.append(requests[request_ids[i]]['text'])
                
    print(f"Cluster 9 Count: {unmapped_counts.get(9, 0)}")
    print("Examples from Cluster 9:")
    for ex in examples:
        print("-", ex.replace('\n', ' '))

if __name__ == "__main__":
    analyze_unmapped()
