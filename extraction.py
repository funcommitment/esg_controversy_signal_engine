import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def extract_article(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        
        # response ifno 
        print(f"  ✓ Status: {resp.status_code} | Response length: {len(resp.text)} chars")
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        article = soup.find("article") or soup.find("div", class_="article-body")
        if article:
            paragraphs = [p.get_text(strip=True) for p in article.find_all("p")]
        else:
            paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        
        raw_text = " ".join(paragraphs)
        
        # extraction result 
        print(f"  ✓ Extracted text: {len(raw_text)} chars | Paragraphs found: {len(paragraphs)}")
        
        if len(raw_text) < 200:
            print(f"  ⚠ Text too short, marking as None")
            raw_text = None
        
        Date = None
        time_tag = soup.find("time")
        if time_tag:
            Date = time_tag.get("datetime") or time_tag.get_text(strip=True)
            print(f"  ✓ Date found: {Date}")
        
        return raw_text, Date
        
    except requests.exceptions.HTTPError as e:
        print(f"  ✗ HTTP Error: {e.response.status_code}")
        return None, None
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout after 10s")
        return None, None
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__} - {e}")
        return None, None

def main():
    df = pd.read_csv("esg.csv", encoding="utf-8")
    url_cache = {}
    
    for i, url in enumerate(df["url"].unique(), 1):
        print(f"\n[{i}/{len(df['url'].unique())}] Fetching: {url}")
        text, Date = extract_article(url)
        url_cache[url] = {"raw_text": text, "Date": Date}
        time.sleep(7)
    
    df["raw_text"] = df["url"].map(lambda u: url_cache[u]["raw_text"])
    df["Date"] = df["url"].map(lambda u: url_cache[u]["Date"])
    
    df.to_csv("esg_articles_with_text.csv", index=False, encoding="utf-8")
    
    total = len(df)
    successful = df["raw_text"].notna().sum()
    failed = total - successful
    print(f"\n{'='*50}")
    print(f"SUMMARY: {successful}/{total} articles extracted successfully ({failed} failed)")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()