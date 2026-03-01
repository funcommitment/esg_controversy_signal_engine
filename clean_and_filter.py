import pandas as pd
import re

MIN_LENGTH = 200

MANUAL_KEEP_URLS = [
    "https://web.archive.org/web/20190325185337/https://www.nationalgeographic.com/environment/2019/03/oil%2Dspills%2D30%2Dyears%2Dafter%2Dexxon%2Dvaldez/",
    "https://www.theguardian.com/environment/2019/oct/09/revealed-20-firms-third-carbon-emissions",
    "http://news.bbc.co.uk/2/hi/europe/4551842.stm",
    "http://news.bbc.co.uk/2/hi/asia-pacific/4465712.stm",
    "https://www.csmonitor.com/1995/1012/12071.html"
]

def clean_text(text):
    """Remove extra whitespace and normalize"""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()

def company_in_text(row):
    company = row["company"].lower()
    text = row["raw_text"].lower()
    url = row["url"]

    if url in MANUAL_KEEP_URLS:
        return True
    
    return company in text

def main():
    df = pd.read_csv("esg_articles_with_text.csv", encoding="utf-8")
    original_len = len(df) 
    
    df = df.dropna(subset=["raw_text"])
    
    df["raw_text"] = df["raw_text"].apply(clean_text)
    
    df["text_length"] = df["raw_text"].str.len()
    df["word_count"] = df["raw_text"].str.split().str.len()
    
    df = df[df["text_length"] > MIN_LENGTH]
    
    before_company_filter = df.copy()
    
    df = df[df.apply(company_in_text, axis=1)]
    
    removed = before_company_filter.loc[~before_company_filter.index.isin(df.index)]
    removed.to_csv("removed_articles_company_filter.csv", index=False, encoding="utf-8")

    df.to_csv("esg_articles_cleaned.csv", index=False, encoding="utf-8")

    print(f"✓ Original: {original_len} articles")
    print(f"✓ Cleaned: {len(df)} articles")
    print(f"✓ Removed (company mismatch): {len(removed)}")
    print(f"✓ Average words: {df['word_count'].mean():.0f}")
    print(f"✓ Shortest: {df['text_length'].min()} chars")
    print(f"✓ Longest: {df['text_length'].max()} chars")

if __name__ == "__main__":
    main()