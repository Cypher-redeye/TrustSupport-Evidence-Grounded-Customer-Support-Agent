import json
import logging
import numpy as np
from pathlib import Path
from collections import defaultdict
from src.config import settings

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_data():
    embed_file = Path(settings.processed_data_dir) / "intent_embeddings.npz"
    if not embed_file.exists():
        return None, None, None
        
    cache = np.load(embed_file)
    embeddings = cache['embeddings']
    request_ids = cache['request_ids']
    
    sample_file = Path(settings.processed_data_dir) / "intent_discovery_sample.jsonl"
    requests = {}
    with open(sample_file, 'r', encoding='utf-8') as f:
        for line in f:
            req = json.loads(line)
            requests[req['request_id']] = req
            
    return embeddings, request_ids, requests

def inspect_clusters():
    embeddings, request_ids, requests = load_data()
    if embeddings is None: return

    out_file = Path("reports") / "intent_cluster_inspection.md"
    
    lines = ["# Intent Cluster Inspection", ""]
    
    for k in [10, 12]:
        logger.info(f"Inspecting K={k}")
        model = KMeans(n_clusters=k, random_state=settings.random_seed, n_init=10)
        labels = model.fit_predict(embeddings)
        centroids = model.cluster_centers_
        
        lines.append(f"## Configuration: KMeans (K={k})")
        lines.append("")
        
        # Group points by cluster
        clusters = defaultdict(list)
        for i, label in enumerate(labels):
            clusters[label].append(i)
            
        for c_id in range(k):
            indices = clusters[c_id]
            size = len(indices)
            
            lines.append(f"### Cluster {c_id} (Size: {size}, {size/len(labels)*100:.1f}%)")
            
            # Find nearest to centroid
            c_embeddings = embeddings[indices]
            centroid = centroids[c_id].reshape(1, -1)
            dists = euclidean_distances(c_embeddings, centroid).flatten()
            
            # Sort by distance
            sorted_idx = np.argsort(dists)
            
            lines.append("#### Top 20 Nearest to Centroid")
            for local_i in sorted_idx[:20]:
                global_i = indices[local_i]
                req_id = request_ids[global_i]
                text = requests[req_id]['text'].replace('\n', ' ')
                lines.append(f"- {text}")
                
            lines.append("")
            
            # Random boundary points (furthest from centroid but still in cluster)
            lines.append("#### 10 Boundary Examples (Furthest)")
            for local_i in sorted_idx[-10:]:
                global_i = indices[local_i]
                req_id = request_ids[global_i]
                text = requests[req_id]['text'].replace('\n', ' ')
                lines.append(f"- {text}")
                
            lines.append("")
            
            # Random 10 examples
            lines.append("#### 10 Random Examples")
            np.random.seed(settings.random_seed + c_id)
            random_idx = np.random.choice(len(sorted_idx), min(10, len(sorted_idx)), replace=False)
            for local_i in random_idx:
                global_i = indices[local_i]
                req_id = request_ids[global_i]
                text = requests[req_id]['text'].replace('\n', ' ')
                lines.append(f"- {text}")
                
            lines.append("")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    logger.info(f"Generated inspection report at {out_file}")

if __name__ == "__main__":
    inspect_clusters()
