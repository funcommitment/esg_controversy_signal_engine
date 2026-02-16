import pandas as pd
from urllib.parse import urlparse

input_file=r"C:\Users\tomar\OneDrive\ドキュメント\esg_project\urls.txt"
output_file="esg.csv"

rows=[]

with open(input_file,"r",encoding="utf-8") as f:
    for line in f:
        line=line.strip()
        try:
            company,url=line.split(",",1)
            domain=urlparse(url).netloc.replace("www.","")

            rows.append({
                "company":company.strip(),
                "url":url.strip(),
                "source_name":domain,
                "raw_text":None,
                "Date":None
            })
        except ValueError:
             print(f"Skipped line: {line}")

df=pd.DataFrame(rows)
df = df.drop_duplicates(subset=["company", "url"])

df.to_csv(output_file, index=False)
print(f"Saved {len(df)} records to {output_file}")