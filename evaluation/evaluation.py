import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_aps(texts):
    if len(texts) < 2:
        return 0.0
        
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    sim_matrix = cosine_similarity(tfidf_matrix)
    N = sim_matrix.shape[0]
    
    sum_sim = np.triu(sim_matrix, k=1).sum()
    aps = (2 * sum_sim) / (N * (N - 1))
    return aps

def get_ngrams(text, n):
    tokens = re.findall(r'\b\w+\b', str(text).lower())
    return set(zip(*[tokens[i:] for i in range(n)]))

def calculate_vocabulary_size(texts):
    unique_tokens = set()
    for text in texts:
        tokens = re.findall(r'\b\w+\b', str(text).lower())
        unique_tokens.update(tokens)
    return len(unique_tokens)

def calculate_ingf(texts, n=3):
    doc_ngrams = [get_ngrams(text, n) for text in texts]
    
    ngram_df = Counter()
    for ngrams in doc_ngrams:
        ngram_df.update(ngrams)
        
    ingf_scores = []
    
    for ngrams in doc_ngrams:
        total_ngrams_in_s = len(ngrams)
        if total_ngrams_in_s == 0:
            continue
            
        overlap_count = sum(1 for g in ngrams if ngram_df[g] > 1)
        score = overlap_count / total_ngrams_in_s
        ingf_scores.append(score)
        
    if not ingf_scores:
        return 0.0
        
    return sum(ingf_scores) / len(ingf_scores)

def evaluate_dataset_diversity(df, dataset_name, text_column='RequirementText'):
    print(f"--- Evaluating Diversity for: {dataset_name} ---")
    
    texts = df[text_column].dropna().astype(str).tolist()
    
    if len(texts) == 0:
        print("The dataset is empty or does not contain valid text.\n")
        return
        
    total_reqs = len(texts)
    vocab_size = calculate_vocabulary_size(texts)
    aps_score = calculate_aps(texts)
    
    ingf_3_score = calculate_ingf(texts, n=3)
    ingf_4_score = calculate_ingf(texts, n=4)
    
    print(f"Total Reqs: {total_reqs}")
    print(f"Unique Tokens (Vocabulary): {vocab_size}")
    print(f"APS    (Semantic Cohesion): {aps_score:.4f}")
    print(f"INGF-3 (Trigram Overlap): {ingf_3_score:.4f}")
    print(f"INGF-4 (4-gram Overlap): {ingf_4_score:.4f}")
    print("-" * 50 + "\n")
    
    return {
        'Dataset': dataset_name, 
        'Total Reqs': total_reqs,
        'Unique Tokens': vocab_size,
        'APS': aps_score, 
        'INGF-3': ingf_3_score,
        'INGF-4': ingf_4_score
    }

if __name__ == "__main__":
    df_promise = pd.read_csv('promise.csv')
    df_sira = pd.read_csv('SIRA.csv')
    df_respan = pd.read_csv('./respan/NFR_English_Final.csv', sep=';')
    
    res_promise = evaluate_dataset_diversity(
        df=df_promise, 
        dataset_name="PROMISE Dataset", 
        text_column='RequirementText'
    )
    
    res_sira = evaluate_dataset_diversity(
        df=df_sira, 
        dataset_name="SIRA Dataset", 
        text_column='requirement_text'
    )
    
    res_respan = evaluate_dataset_diversity(
        df=df_respan, 
        dataset_name="ReSpaN Dataset", 
        text_column='Requirement'
    )
    
    results_df = pd.DataFrame([res_promise, res_sira, res_respan])
    print("Summary to include in the paper:")
    print(results_df.to_markdown(index=False))
