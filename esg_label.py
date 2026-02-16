import pandas as pd
import re

ENV_KEYWORDS = [
    "pollution", "spill", "emission", "carbon", "greenhouse", "climate",
    "environmental", "toxic", "waste", "contamination", "deforestation",
    "biodiversity", "oil spill", "methane", "co2", "renewable", "fossil fuel",
    "drilling", "pipeline", "acid rain", "hazardous", "ecosystem"
]

SOCIAL_KEYWORDS = [
    "human rights", "labor", "worker", "employee", "community", "indigenous",
    "health", "safety", "discrimination", "exploitation", "forced labor",
    "child labor", "protest", "union", "wages", "injury", "fatality",
    "displacement", "poverty", "social", "lawsuit", "victims","cancer", 
    "disease", "residents", "evacuation","compensation", "suffering", "affected", "exposure",
    "respiratory", "contaminated water", "public health"
]

GOV_KEYWORDS = [
    "corruption", "fraud", "bribery", "misconduct", "scandal", "fine",
    "penalty", "lawsuit", "litigation", "settlement", "investigation",
    "regulatory", "compliance", "governance", "accountability", "sanction",
    "violation", "illegal", "court", "ruling", "conviction", "indictment", 
    "pension", "deficit", "shareholder", "dividend", "financial", "liability", "fiduciary"
]


def count_keywords(text, keywords):
    if not isinstance(text, str):
        return 0
    text = text.lower()
    count = 0
    for keyword in keywords:
        # Use word boundary for single words, direct match for phrases
        if " " in keyword:
            count += len(re.findall(re.escape(keyword), text))
        else:
            count += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
    return count

def get_esg_category(env, social, gov):
    """Assign dominant ESG category based on highest score"""
    scores = {"Environmental": env, "Social": social, "Governance": gov}
    if max(scores.values()) == 0:
        return "Unclassified"
    return max(scores, key=scores.get)

def main():
    df = pd.read_csv("esg_articles_cleaned.csv", encoding="utf-8")
    
    print(f"Processing {len(df)} articles...")
    
    # score each 
    df["env_score"]    = df["raw_text"].apply(lambda x: count_keywords(x, ENV_KEYWORDS))
    df["social_score"] = df["raw_text"].apply(lambda x: count_keywords(x, SOCIAL_KEYWORDS))
    df["gov_score"]    = df["raw_text"].apply(lambda x: count_keywords(x, GOV_KEYWORDS))
    
    # dominant category 
    df["esg_category"] = df.apply(
        lambda row: get_esg_category(row["env_score"], row["social_score"], row["gov_score"]),
        axis=1
    )

    df["is_env"]  = df["env_score"] > 5
    df["is_social"] = df["social_score"] > 5
    df["is_gov"]  = df["gov_score"] > 5
    
    # normalize scores for fairness
    df["env_score_norm"]    = (df["env_score"]    / df["raw_text"].str.len() * 1000).round(3)
    df["social_score_norm"] = (df["social_score"] / df["raw_text"].str.len() * 1000).round(3)
    df["gov_score_norm"]    = (df["gov_score"]    / df["raw_text"].str.len() * 1000).round(3)
    
    df.to_csv("esg_articles_tagged.csv", index=False, encoding="utf-8")
    
    print(f"\n{'='*50}")
    print(f"TAGGING SUMMARY")
    print(f"{'='*50}")
    print(f"Total articles tagged: {len(df)}")
    print(f"\nESG Category Distribution:")
    print(df["esg_category"].value_counts().to_string())
    print(f"\nAverage Scores:")
    print(f"  Environmental : {df['env_score'].mean():.2f}")
    print(f"  Social        : {df['social_score'].mean():.2f}")
    print(f"  Governance    : {df['gov_score'].mean():.2f}")
    print(f"\nTop 5 articles by ENV score:")
    print(df[["company", "env_score", "esg_category"]].sort_values("env_score", ascending=False).head())
    # Check the unclassified article
    print(df[df["esg_category"] == "Unclassified"][["company", "url", "raw_text"]].values)
    # Check why social is so low
    print(df[["company", "social_score"]].sort_values("social_score", ascending=False).head(10))

if __name__ == "__main__":
    main()