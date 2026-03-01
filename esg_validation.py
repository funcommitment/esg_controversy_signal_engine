from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd

df = pd.read_csv("esg_articles_final.csv")

# Convert TRUE/FALSE text to 1/0 for predicted columns
df['is_env'] = (df['is_env'] == True).astype(int)
df['is_social'] = (df['is_social'] == True).astype(int)
df['is_gov'] = (df['is_gov'] == True).astype(int)

# Calculate metrics for each category
print("ESG Keyword Tagging Performance Evaluation")
print("=" * 50)

for cat in ['env', 'social', 'gov']:
    pred_col = f'is_{cat}'
    true_col = f'true_{cat}'
    
    precision = precision_score(df[true_col], df[pred_col])
    recall = recall_score(df[true_col], df[pred_col])
    f1 = f1_score(df[true_col], df[pred_col])
    
    print(f"\n{cat.upper()}:")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall:    {recall:.3f}")
    print(f"  F1-Score:  {f1:.3f}")

print(f"\n{'=' * 50}")
print(f"Total articles evaluated: {len(df)}")