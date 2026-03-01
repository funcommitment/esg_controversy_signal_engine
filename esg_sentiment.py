import pandas as pd
from transformers import pipeline
import torch
from collections import Counter

print("Loading FinBERT model...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert",
    device=0 if torch.cuda.is_available() else -1
)

def get_sentiment(text):
    if not isinstance(text, str) or len(text) == 0:
        return None, None

    # split into chunk of 400 words
    words   = text.split()
    chunks  = []
    current = []
    count   = 0

    for word in words:
        current.append(word)
        count += 1
        if count >= 400:
            chunks.append(" ".join(current))
            current = []
            count   = 0
    if current:
        chunks.append(" ".join(current))

    results   = sentiment_pipeline(chunks, truncation=True, max_length=512)
    score_map = {"positive": 1, "neutral": 0, "negative": -1}
    scores    = [score_map.get(r["label"], 0) * r["score"] for r in results]
    labels    = [r["label"] for r in results]
    avg_score = sum(scores) / len(scores)
    dominant  = Counter(labels).most_common(1)[0][0]

    return round(avg_score, 4), dominant

def main():
    df = pd.read_csv("esg_articles_tagged.csv", encoding="utf-8")

    print(f"Running sentiment analysis on {len(df)} articles...")
    print("(This may take a few minutes on CPU)\n")

    sentiments = []
    for i, row in df.iterrows():
        print(f"  [{i+1}/{len(df)}] {row['company']} - {row['url'][:60]}...")
        score, label = get_sentiment(row["raw_text"])
        sentiments.append({"sentiment_score": score, "sentiment_label": label})

    sentiment_df          = pd.DataFrame(sentiments)
    df["sentiment_score"] = sentiment_df["sentiment_score"]
    df["sentiment_label"] = sentiment_df["sentiment_label"]

    company_sentiment = df.groupby("company").agg(
        avg_sentiment     = ("sentiment_score", "mean"),
        negative_articles = ("sentiment_label", lambda x: (x == "negative").sum()),
        positive_articles = ("sentiment_label", lambda x: (x == "positive").sum()),
        neutral_articles  = ("sentiment_label", lambda x: (x == "neutral").sum()),
    ).round(4).reset_index()

    df.to_csv("esg_articles_final.csv", index=False, encoding="utf-8")
    company_sentiment.to_csv("esg_company_sentiment.csv", index=False, encoding="utf-8")

    # summary
    print(f"\n{'='*55}")
    print(f"SENTIMENT ANALYSIS SUMMARY")
    print(f"{'='*55}")
    print(f"\nArticle-level sentiment distribution:")
    print(df["sentiment_label"].value_counts().to_string())
    print(f"\nCompany sentiment ranking (most negative first):")
    print(company_sentiment.sort_values("avg_sentiment")[
        ["company", "avg_sentiment", "negative_articles",
         "positive_articles", "neutral_articles"]
    ].to_string(index=False))

    #  check 2 positive articles
    print(f"\n{'='*55}")
    print(f"VALIDATION: Positive Articles (suspicious - check these!)")
    print(f"{'='*55}")
    positive_articles = df[df["sentiment_label"] == "positive"]
    if len(positive_articles) > 0:
        for _, row in positive_articles.iterrows():
            print(f"\nCompany : {row['company']}")
            print(f"URL     : {row['url']}")
            print(f"Score   : {row['sentiment_score']}")
            print(f"Preview : {str(row['raw_text'])[:300]}...")
    else:
        print("No positive articles found.")

    # corelation check 
    print(f"\n{'='*55}")
    print(f"VALIDATION: Score Correlations")
    print(f"{'='*55}")
    print(df[["env_score", "social_score", "gov_score",
              "sentiment_score"]].corr().round(3).to_string())

    # check most negative articles
    print(f"\n{'='*55}")
    print(f"VALIDATION: Top 5 Most Negative Articles")
    print(f"{'='*55}")
    top_negative = df.nsmallest(5, "sentiment_score")[
        ["company", "sentiment_score", "sentiment_label", "url"]
    ]
    print(top_negative.to_string(index=False))

    # most neutral articles(potential misclassification )
    print(f"\n{'='*55}")
    print(f"VALIDATION: Neutral Articles with High ESG Scores (potential misclassifications)")
    print(f"{'='*55}")
    suspicious = df[
        (df["sentiment_label"] == "neutral") &
        (df["env_score"] + df["social_score"] + df["gov_score"] > 20)
    ][["company", "url", "sentiment_score", "env_score", "social_score", "gov_score"]]
    print(suspicious.to_string(index=False))

if __name__ == "__main__":
    main()