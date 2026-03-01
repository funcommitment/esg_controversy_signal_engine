import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

df = pd.read_csv("esg_company_scores.csv")
df = df.sort_values("final_score", ascending=False)

plt.rcParams.update({
    "figure.facecolor": "#0f1318",
    "axes.facecolor":   "#0f1318",
    "axes.edgecolor":   "#1e2530",
    "axes.labelcolor":  "#94a3b8",
    "xtick.color":      "#94a3b8",
    "ytick.color":      "#94a3b8",
    "text.color":       "#e2e8f0",
    "grid.color":       "#1e2530",
    "grid.linestyle":   "--",
    "font.family":      "monospace",
    "font.size":        9,
})

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("ESG Company Risk Analysis — Final Scores", fontsize=14,
             fontweight="bold", color="#e2e8f0", y=1.02)

companies = df["company"].tolist()
colors = ["#ef4444" if t == "High Risk" else "#f97316" if t == "Medium Risk"
          else "#22c55e" for t in df["risk_tier"]]

# Plot 1: Bar chart → company vs final_score 
ax1 = axes[0]
bars = ax1.barh(companies, df["final_score"], color=colors, height=0.6)
ax1.set_title("Final ESG Risk Score by Company", color="#e2e8f0", pad=10)
ax1.set_xlabel("Final Score (Severity + Volume + Sentiment)")
ax1.invert_yaxis()
ax1.grid(axis="x", alpha=0.3)
for bar, val in zip(bars, df["final_score"]):
    ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
             f"{val:.3f}", va="center", fontsize=8, color="#94a3b8")

# Plot 2: Stacked bar → ENV/SOC/GOV totals per company
ax2 = axes[1]
env_vals    = df["total_env_score"].tolist()
social_vals = df["total_social_score"].tolist()
gov_vals    = df["total_gov_score"].tolist()
x = range(len(companies))

ax2.bar(x, env_vals,    color="#22c55e", label="Environmental", width=0.6)
ax2.bar(x, social_vals, color="#3b82f6", label="Social",        width=0.6, bottom=env_vals)
ax2.bar(x, gov_vals,    color="#f59e0b", label="Governance",    width=0.6,
        bottom=[e+s for e, s in zip(env_vals, social_vals)])

ax2.set_title("ESG Score Breakdown per Company", color="#e2e8f0", pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(companies, rotation=45, ha="right", fontsize=8)
ax2.set_ylabel("Total Score")
ax2.grid(axis="y", alpha=0.3)
ax2.legend(loc="upper right", fontsize=8,
           facecolor="#0f1318", edgecolor="#1e2530", labelcolor="#e2e8f0")

# Plot 3: Scatter → total_articles vs final_score
ax3 = axes[2]
ax3.scatter(df["total_articles"], df["final_score"],
            c=colors, s=100, zorder=5, edgecolors="#0f1318", linewidth=0.5)

for _, row in df.iterrows():
    ax3.annotate(row["company"],
                 (row["total_articles"], row["final_score"]),
                 textcoords="offset points", xytext=(6, 4),
                 fontsize=7.5, color="#94a3b8")

ax3.set_title("Article Volume vs Final Risk Score", color="#e2e8f0", pad=10)
ax3.set_xlabel("Total Articles")
ax3.set_ylabel("Final Score")
ax3.grid(alpha=0.3)

# Shared legend
legend_elements = [
    Patch(facecolor="#ef4444", label="High Risk"),
    Patch(facecolor="#f97316", label="Medium Risk"),
    Patch(facecolor="#22c55e", label="Low Risk"),
]
fig.legend(handles=legend_elements, loc="lower center", ncol=3,
           fontsize=9, facecolor="#0f1318", edgecolor="#1e2530",
           labelcolor="#e2e8f0", bbox_to_anchor=(0.5, -0.05))

plt.tight_layout()
plt.savefig("esg_risk_analysis.png", dpi=150, bbox_inches="tight",
            facecolor="#0f1318")
plt.show()
print("✓ Saved as esg_risk_analysis.png")