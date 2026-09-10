import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from src.config import settings

from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def try_hdbscan():
    try:
        from sklearn.cluster import HDBSCAN
        return HDBSCAN, "HDBSCAN"
    except ImportError:
        logger.warning("HDBSCAN not available in this sklearn version. Falling back to DBSCAN.")
        return DBSCAN, "DBSCAN"

def load_data():
    embed_file = Path(settings.processed_data_dir) / "intent_embeddings.npz"
    if not embed_file.exists():
        logger.error("Embeddings not found.")
        return None, None
        
    cache = np.load(embed_file)
    embeddings = cache['embeddings']
    request_ids = cache['request_ids']
    return embeddings, request_ids

def run_clustering():
    embeddings, request_ids = load_data()
    if embeddings is None: return

    logger.info(f"Loaded {len(embeddings)} embeddings for clustering experiments.")
    
    results = []
    
    # K-Means Experiments
    k_values = [6, 8, 10, 12, 15]
    for k in k_values:
        logger.info(f"Running KMeans with K={k}")
        model = KMeans(n_clusters=k, random_state=settings.random_seed, n_init=10)
        labels = model.fit_predict(embeddings)
        
        sil = silhouette_score(embeddings, labels)
        db = davies_bouldin_score(embeddings, labels)
        
        sizes = dict(Counter(labels))
        max_cluster_pct = max(sizes.values()) / len(labels)
        noise_pct = 0.0 # KMeans has no noise
        
        results.append({
            'Algorithm': 'KMeans',
            'Config': f"K={k}",
            'Silhouette': sil,
            'DaviesBouldin': db,
            'NumClusters': k,
            'MaxClusterPct': max_cluster_pct,
            'NoisePct': noise_pct
        })
        
    # Density Based Experiment
    DensityModel, model_name = try_hdbscan()
    logger.info(f"Running {model_name}")
    if model_name == "HDBSCAN":
        model = DensityModel(min_cluster_size=15, min_samples=5)
    else:
        # Fallback to DBSCAN (eps might need tuning, typical cosine dist range is small, 
        # but euclidean on normalized vectors can be ~0.5 to 1.0)
        # We will normalize embeddings for DBSCAN
        from sklearn.preprocessing import normalize
        norm_emb = normalize(embeddings)
        model = DensityModel(eps=0.5, min_samples=10)
        embeddings = norm_emb # Use normalized for metrics
        
    labels = model.fit_predict(embeddings)
    
    # Filter noise for metrics (-1 is noise)
    valid_mask = labels != -1
    if sum(valid_mask) > 1: # need at least 2 points to score
        sil = silhouette_score(embeddings[valid_mask], labels[valid_mask])
        db = davies_bouldin_score(embeddings[valid_mask], labels[valid_mask])
    else:
        sil = -1
        db = -1
        
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    sizes = dict(Counter(labels))
    noise_pct = sizes.get(-1, 0) / len(labels)
    max_cluster_pct = max([v for k,v in sizes.items() if k != -1] + [0]) / len(labels)
    
    results.append({
        'Algorithm': model_name,
        'Config': 'default',
        'Silhouette': sil,
        'DaviesBouldin': db,
        'NumClusters': n_clusters,
        'MaxClusterPct': max_cluster_pct,
        'NoisePct': noise_pct
    })
    
    df = pd.DataFrame(results)
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    out_csv = out_dir / "intent_clustering_metrics.csv"
    df.to_csv(out_csv, index=False)
    logger.info(f"Saved clustering metrics to {out_csv}")
    
    # Output to stdout for quick review
    print("\nClustering Metrics:")
    print(df.to_markdown())

if __name__ == "__main__":
    run_clustering()
