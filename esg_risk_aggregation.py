import pandas as pd
import numpy as np

def main():
    df = pd.read_csv("esg_articles_tagged.csv", encoding="utf-8")
    
    company_agg = df.groupby("company").agg(
        total_articles     = ("raw_text", "count"),
        total_env_score    = ("env_score", "sum"),
        total_social_score = ("social_score", "sum"),
        total_gov_score    = ("gov_score", "sum"),
        avg_env_norm       = ("env_score_norm", "mean"),
        avg_social_norm    = ("social_score_norm", "mean"),
        avg_gov_norm       = ("gov_score_norm", "mean"),
        env_articles       = ("is_env", "sum"),
        social_articles    = ("is_social", "sum"),
        gov_articles       = ("is_gov", "sum"),
    ).reset_index()
    
    #Controversy score (severity + volume)
    severity = (
        (company_agg["avg_env_norm"]    * 0.5) +
        (company_agg["avg_social_norm"] * 0.3) +
        (company_agg["avg_gov_norm"]    * 0.2)
    )
    volume = np.log1p(company_agg["total_articles"])
    
    company_agg["controversy_score"] = (
        (severity * 0.7) + (volume * 0.3)
    ).round(3)
    
    #merge sentiment scores
    sentiment_df = pd.read_csv("esg_company_sentiment.csv")
    company_agg  = company_agg.merge(sentiment_df, on="company", how="left")
    
    # Final score (controversy + sentiment)
    company_agg["final_score"] = (
        company_agg["controversy_score"] * 0.7 +
        abs(company_agg["avg_sentiment"]).fillna(0) * 0.3
    ).round(3)
    
    # Rank companies by final score
    company_agg = company_agg.sort_values("final_score", ascending=False)
    company_agg["risk_rank"] = range(1, len(company_agg) + 1)
    
    # Risk tier
    company_agg["risk_tier"] = pd.cut(
        company_agg["final_score"],
        bins=3,
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )
    
    company_agg.to_csv("esg_company_scores.csv", index=False, encoding="utf-8")
    
    print(f"\n{'='*55}")
    print(f"ESG COMPANY RISK RANKING")
    print(f"{'='*55}")
    print(company_agg[["risk_rank", "company", "total_articles",
                        "controversy_score", "avg_sentiment",
                        "final_score", "risk_tier"]].to_string(index=False))
    print(f"\nDetailed Scores:")
    print(company_agg[["company", "total_env_score",
                        "total_social_score", "total_gov_score",
                        "env_articles", "social_articles",
                        "gov_articles"]].to_string(index=False))
    print(f"\nSeverity vs Volume vs Sentiment Breakdown:")
    company_agg["severity_component"]  = (severity * 0.7).round(3)
    company_agg["volume_component"]    = (volume   * 0.3).round(3)
    company_agg["sentiment_component"] = (abs(company_agg["avg_sentiment"]) * 0.3).round(3)
    print(company_agg[["company", "severity_component", "volume_component",
                        "sentiment_component", "final_score"]].to_string(index=False))

if __name__ == "__main__":
    main()