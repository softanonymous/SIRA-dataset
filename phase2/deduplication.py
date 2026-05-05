import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

print("Loading data and model...")
df = pd.read_csv('../SIRA.csv')
model = SentenceTransformer('all-mpnet-base-v2')

thresholds = [0.8]

indices_to_delete_by_threshold = {t: set() for t in thresholds}

label_counts = df['label'].value_counts()
print("\n--- Requirements Summary by Class (Label) ---")
print(label_counts.to_string())
print("-" * 45)

for label in label_counts.index:
    df_label = df[df['label'] == label]
    total_reqs = len(df_label)
    
    print(f"\nProcessing class: {label} (Total: {total_reqs} reqs)")

    if total_reqs < 2:
        continue

    texts = df_label['requirement_text'].tolist()
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=False, convert_to_tensor=True)

    global_indices = df_label.index.tolist()

    for threshold in thresholds:
        clusters = util.community_detection(embeddings, min_community_size=2, threshold=threshold)
        
        for cluster in clusters:
            for local_idx in cluster[1:]:
                global_idx = global_indices[local_idx]
                indices_to_delete_by_threshold[threshold].add(global_idx)

print(f"\n{'='*60}")
print("=== DELETION SUMMARY BY THRESHOLD ===")
print(f"{'='*60}")

for threshold in thresholds:
    indices_to_delete = list(indices_to_delete_by_threshold[threshold])
    
    df_clean = df.drop(index=indices_to_delete)
    df_deleted = df.loc[indices_to_delete]
    
    str_threshold = str(threshold).replace(".", "")
    clean_file = f'clean_reqs_tol_{str_threshold}.csv'
    deleted_file = f'deleted_reqs_tol_{str_threshold}.csv'
    
    df_clean.to_csv(clean_file, index=False)
    df_deleted.to_csv(deleted_file, index=False)
    
    print(f"Threshold {threshold}:")
    print(f"  - Preserved requirements : {len(df_clean)}")
    print(f"  - Deleted requirements   : {len(df_deleted)}")
    print(f"  -> Generated: {clean_file} and {deleted_file}\n")

print("Process completed successfully.")
