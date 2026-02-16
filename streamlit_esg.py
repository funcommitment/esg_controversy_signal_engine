import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ESG Controversy Signal Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Crimson Pro', Georgia, serif;
    background-color: #080b0f;
    color: #dde3ed;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: #080b0f;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #0f1318 0%, #0a0d11 50%, #0f1318 100%);
    border: 1px solid #1a2030;
    border-left: 4px solid #dc2626;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(ellipse at right, rgba(220,38,38,0.06), transparent 70%);
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 0.06em;
    color: #f1f5f9;
    line-height: 1;
    margin: 0;
}

.hero-title span {
    color: #dc2626;
}

.hero-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: #475569;
    margin-top: 0.5rem;
    text-transform: uppercase;
}

.hero-desc {
    font-size: 1.05rem;
    color: #94a3b8;
    margin-top: 0.8rem;
    max-width: 700px;
    line-height: 1.6;
    font-style: italic;
}

/* Metric cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: #0d1117;
    border: 1px solid #1a2030;
    padding: 1.2rem 1.4rem;
    position: relative;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}

.metric-card.red::after   { background: #dc2626; }
.metric-card.orange::after { background: #ea580c; }
.metric-card.blue::after  { background: #2563eb; }
.metric-card.green::after { background: #16a34a; }

.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    line-height: 1;
}

.metric-card.red .metric-value   { color: #dc2626; }
.metric-card.orange .metric-value { color: #ea580c; }
.metric-card.blue .metric-value  { color: #2563eb; }
.metric-card.green .metric-value { color: #16a34a; }

.metric-sub {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 0.2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Section headers */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1a2030;
}

/* Risk badge */
.risk-high   { color: #dc2626; font-weight: 600; }
.risk-medium { color: #ea580c; font-weight: 600; }
.risk-low    { color: #16a34a; font-weight: 600; }

/* Company card */
.company-card {
    background: #0d1117;
    border: 1px solid #1a2030;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s;
}

.company-card:hover {
    border-color: #dc2626;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0a0d11 !important;
    border-right: 1px solid #1a2030;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data_testid="stSidebar"] .stMultiSelect label {
    color: #94a3b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
}

/* Dataframe */
.stDataFrame {
    background: #0d1117 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117;
    border-bottom: 1px solid #1a2030;
    gap: 0;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    padding: 0.8rem 1.5rem;
    border-bottom: 2px solid transparent;
}

.stTabs [aria-selected="true"] {
    color: #f1f5f9 !important;
    border-bottom: 2px solid #dc2626 !important;
    background: transparent !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #0d1117 !important;
    border: 1px solid #1a2030 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #94a3b8 !important;
}

/* Info boxes */
.info-box {
    background: rgba(37, 99, 235, 0.08);
    border: 1px solid rgba(37, 99, 235, 0.25);
    border-left: 3px solid #2563eb;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #93c5fd;
    font-family: 'JetBrains Mono', monospace;
}

.warn-box {
    background: rgba(220, 38, 38, 0.08);
    border: 1px solid rgba(220, 38, 38, 0.25);
    border-left: 3px solid #dc2626;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #fca5a5;
    font-family: 'JetBrains Mono', monospace;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #1a2030;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        scores    = pd.read_csv("esg_company_scores.csv")
        articles  = pd.read_csv("esg_articles_final.csv")
        sentiment = pd.read_csv("esg_company_sentiment.csv")
        return scores, articles, sentiment
    except FileNotFoundError as e:
        st.error(f"⚠️ Data file not found: {e}. Make sure all pipeline CSVs are present.")
        st.stop()

scores_df, articles_df, sentiment_df = load_data()

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0d1117",
    "axes.facecolor":    "#0d1117",
    "axes.edgecolor":    "#1a2030",
    "axes.labelcolor":   "#64748b",
    "xtick.color":       "#64748b",
    "ytick.color":       "#64748b",
    "text.color":        "#dde3ed",
    "grid.color":        "#1a2030",
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.family":       "monospace",
    "font.size":         8.5,
})

COLORS = {
    "High Risk":   "#dc2626",
    "Medium Risk": "#ea580c",
    "Low Risk":    "#16a34a",
    "env":         "#16a34a",
    "social":      "#2563eb",
    "gov":         "#ca8a04",
    "accent":      "#dc2626",
    "muted":       "#475569",
}


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0;'>
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.6rem; color: #dc2626; letter-spacing: 0.08em;'>
            ESG ENGINE
        </div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 0.6rem; color: #475569; letter-spacing: 0.2em; margin-top: 0.2rem;'>
            SIGNAL INTELLIGENCE v1.0
        </div>
    </div>
    <hr style='border-color: #1a2030; margin: 0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-family: JetBrains Mono, monospace; font-size: 0.65rem; color: #475569; letter-spacing: 0.15em; text-transform: uppercase;'>Filter by Risk Tier</p>", unsafe_allow_html=True)
    
    selected_tiers = st.multiselect(
        "", 
        options=["High Risk", "Medium Risk", "Low Risk"],
        default=["High Risk", "Medium Risk", "Low Risk"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: JetBrains Mono, monospace; font-size: 0.65rem; color: #475569; letter-spacing: 0.15em; text-transform: uppercase;'>Select Company</p>", unsafe_allow_html=True)
    
    all_companies = sorted(scores_df["company"].tolist())
    selected_company = st.selectbox(
        "", 
        options=["All Companies"] + all_companies,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: JetBrains Mono, monospace; font-size: 0.65rem; color: #475569; letter-spacing: 0.15em; text-transform: uppercase;'>Score Threshold</p>", unsafe_allow_html=True)
    
    min_score = st.slider(
        "", 
        min_value=0.0, 
        max_value=float(scores_df["final_score"].max()),
        value=0.0, 
        step=0.05,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color: #1a2030;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family: JetBrains Mono, monospace; font-size: 0.6rem; color: #475569; line-height: 2;'>
        <div>📡 SOURCE: Public News Articles</div>
        <div>🏭 SECTOR: Oil & Gas</div>
        <div>🤖 MODEL: FinBERT (ProsusAI)</div>
        <div>📊 ARTICLES: 81 scraped</div>
        <div>🏢 COMPANIES: 10 covered</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(220,38,38,0.08); border: 1px solid rgba(220,38,38,0.2); padding: 0.8rem; font-family: JetBrains Mono, monospace; font-size: 0.6rem; color: #fca5a5;'>
        ⚠️ PROTOTYPE ONLY<br>Not for investment decisions
    </div>
    """, unsafe_allow_html=True)


# ── Filter data ───────────────────────────────────────────────────────────────
filtered_scores = scores_df[
    (scores_df["risk_tier"].isin(selected_tiers)) &
    (scores_df["final_score"] >= min_score)
].copy()

if selected_company != "All Companies":
    company_articles = articles_df[articles_df["company"] == selected_company]
else:
    company_articles = articles_df


# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">ESG <span>CONTROVERSY</span> SIGNAL ENGINE</div>
    <div class="hero-subtitle">Oil & Gas · NLP Risk Intelligence · Analyst Decision Support</div>
    <div class="hero-desc">
        Automated detection and scoring of ESG controversy signals from public news sources.
        Combining keyword severity, article volume, and FinBERT sentiment into actionable risk rankings.
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# METRIC CARDS
# ══════════════════════════════════════════════════════════════════════════════
high_risk_count  = len(scores_df[scores_df["risk_tier"] == "High Risk"])
total_articles   = int(scores_df["total_articles"].sum())
neg_articles     = len(articles_df[articles_df["sentiment_label"] == "negative"]) if "sentiment_label" in articles_df.columns else 51
avg_score        = scores_df["final_score"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card red">
        <div class="metric-label">High Risk Companies</div>
        <div class="metric-value">{high_risk_count}</div>
        <div class="metric-sub">of {len(scores_df)} total covered</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-label">Articles Analyzed</div>
        <div class="metric-value">{total_articles}</div>
        <div class="metric-sub">87% scraping success rate</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Negative Sentiment</div>
        <div class="metric-value">{neg_articles}</div>
        <div class="metric-sub">articles flagged negative</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Avg Risk Score</div>
        <div class="metric-value">{avg_score:.3f}</div>
        <div class="metric-sub">across all companies</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  RISK RANKINGS",
    "🔬  ESG BREAKDOWN", 
    "💬  SENTIMENT ANALYSIS",
    "📰  ARTICLE EXPLORER",
    "⚙️  METHODOLOGY"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: RISK RANKINGS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Final ESG Risk Ranking — Severity + Volume + Sentiment</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        # Horizontal bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")

        sorted_df = filtered_scores.sort_values("final_score", ascending=True)
        bar_colors = [COLORS.get(t, "#475569") for t in sorted_df["risk_tier"]]

        bars = ax.barh(sorted_df["company"], sorted_df["final_score"],
                       color=bar_colors, height=0.55, zorder=3)

        # Controversy score overlay (ghost bars)
        ax.barh(sorted_df["company"], sorted_df["controversy_score"],
                color=[c + "22" for c in bar_colors], height=0.55,
                zorder=2, linewidth=0)

        ax.set_xlabel("Final Risk Score", color="#475569", fontsize=8)
        ax.set_title("Company ESG Risk Ranking", color="#dde3ed",
                     fontsize=10, fontweight="bold", pad=12)
        ax.grid(axis="x", zorder=0)
        ax.spines[["top", "right", "left"]].set_visible(False)

        for bar, val in zip(bars, sorted_df["final_score"]):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f"{val:.3f}", va="center", fontsize=7.5,
                    color="#94a3b8", fontfamily="monospace")

        legend_patches = [
            mpatches.Patch(color=COLORS["High Risk"],   label="High Risk"),
            mpatches.Patch(color=COLORS["Medium Risk"], label="Medium Risk"),
            mpatches.Patch(color=COLORS["Low Risk"],    label="Low Risk"),
        ]
        ax.legend(handles=legend_patches, loc="lower right",
                  facecolor="#0d1117", edgecolor="#1a2030",
                  labelcolor="#dde3ed", fontsize=7)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

    with col_right:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Ranking table
        display_cols = ["risk_rank", "company", "final_score", "risk_tier", "total_articles"]
        display_df = filtered_scores[display_cols].copy()
        display_df.columns = ["Rank", "Company", "Score", "Risk Tier", "Articles"]
        display_df = display_df.sort_values("Rank")

        def color_tier(val):
            if val == "High Risk":   return "color: #dc2626; font-weight: bold"
            elif val == "Medium Risk": return "color: #ea580c; font-weight: bold"
            else: return "color: #16a34a; font-weight: bold"

        styled = display_df.style\
            .applymap(color_tier, subset=["Risk Tier"])\
            .format({"Score": "{:.3f}"})\
            .set_properties(**{
                "background-color": "#0d1117",
                "color": "#dde3ed",
                "font-family": "JetBrains Mono, monospace",
                "font-size": "12px"
            })\
            .hide(axis="index")

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=380)

        # Score formula explanation
        st.markdown("""
        <div class="info-box">
            <b>Score Formula:</b><br>
            final = (controversy × 0.7) + (|sentiment| × 0.3)<br>
            controversy = (severity × 0.7) + (log(volume) × 0.3)
        </div>
        """, unsafe_allow_html=True)

    # Scatter plot
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Volume vs Severity — Bubble Analysis</div>', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(12, 4))
    scatter_colors = [COLORS.get(t, "#475569") for t in filtered_scores["risk_tier"]]
    bubble_sizes   = (filtered_scores["total_articles"] * 25).clip(50, 500)

    scatter = ax2.scatter(
        filtered_scores["total_articles"],
        filtered_scores["final_score"],
        c=scatter_colors, s=bubble_sizes,
        alpha=0.85, zorder=5,
        edgecolors="#080b0f", linewidth=1.5
    )

    for _, row in filtered_scores.iterrows():
        ax2.annotate(
            row["company"],
            (row["total_articles"], row["final_score"]),
            textcoords="offset points", xytext=(8, 5),
            fontsize=7.5, color="#94a3b8", fontfamily="monospace"
        )

    ax2.set_xlabel("Total Articles (Volume)", color="#475569")
    ax2.set_ylabel("Final Risk Score", color="#475569")
    ax2.set_title("Bubble size = Article Count  |  Color = Risk Tier",
                  color="#475569", fontsize=8, style="italic")
    ax2.grid(alpha=0.3)
    ax2.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: ESG BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Environmental · Social · Governance Score Breakdown</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Stacked bar
        fig3, ax3 = plt.subplots(figsize=(7, 5))
        sorted_esg = filtered_scores.sort_values("final_score", ascending=False)
        x     = np.arange(len(sorted_esg))
        env   = sorted_esg["total_env_score"].values
        soc   = sorted_esg["total_social_score"].values
        gov   = sorted_esg["total_gov_score"].values

        b1 = ax3.bar(x, env, color=COLORS["env"],    label="Environmental", width=0.6, zorder=3)
        b2 = ax3.bar(x, soc, color=COLORS["social"], label="Social",        width=0.6, bottom=env, zorder=3)
        b3 = ax3.bar(x, gov, color=COLORS["gov"],    label="Governance",    width=0.6,
                     bottom=env + soc, zorder=3)

        ax3.set_xticks(x)
        ax3.set_xticklabels(sorted_esg["company"], rotation=35, ha="right", fontsize=7.5)
        ax3.set_ylabel("Cumulative Keyword Score")
        ax3.set_title("Total ESG Keyword Scores per Company", color="#dde3ed",
                      fontsize=9, fontweight="bold")
        ax3.legend(facecolor="#0d1117", edgecolor="#1a2030",
                   labelcolor="#dde3ed", fontsize=7)
        ax3.grid(axis="y", zorder=0)
        ax3.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        plt.close()

    with col_b:
        # Category distribution donut
        env_total   = int(filtered_scores["env_articles"].sum())
        soc_total   = int(filtered_scores["social_articles"].sum())
        gov_total   = int(filtered_scores["gov_articles"].sum())

        fig4, ax4 = plt.subplots(figsize=(5, 5))
        wedge_data   = [env_total, soc_total, gov_total]
        wedge_colors = [COLORS["env"], COLORS["social"], COLORS["gov"]]
        wedge_labels = [f"Environmental\n{env_total}", f"Social\n{soc_total}", f"Governance\n{gov_total}"]

        wedges, texts, autotexts = ax4.pie(
            wedge_data,
            labels=wedge_labels,
            colors=wedge_colors,
            autopct="%1.0f%%",
            pctdistance=0.75,
            startangle=90,
            wedgeprops={"width": 0.55, "edgecolor": "#080b0f", "linewidth": 2}
        )

        for text in texts:
            text.set_color("#94a3b8")
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color("#dde3ed")
            autotext.set_fontsize(8)
            autotext.set_fontweight("bold")

        ax4.set_title("ESG Article Category Distribution", color="#dde3ed",
                      fontsize=9, fontweight="bold", pad=15)

        plt.tight_layout()
        st.pyplot(fig4, use_container_width=True)
        plt.close()

    # Normalized scores heatmap-style
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Normalized Score Intensity — Per 1000 Characters</div>', unsafe_allow_html=True)

    norm_cols = ["company", "avg_env_norm", "avg_social_norm", "avg_gov_norm", "controversy_score", "final_score"]
    if all(c in filtered_scores.columns for c in norm_cols):
        norm_df = filtered_scores[norm_cols].copy()
        norm_df.columns = ["Company", "ENV/1000", "SOCIAL/1000", "GOV/1000", "Controversy", "Final Score"]
        norm_df = norm_df.sort_values("Final Score", ascending=False)

        styled_norm = norm_df.style\
            .background_gradient(subset=["ENV/1000"], cmap="Greens")\
            .background_gradient(subset=["SOCIAL/1000"], cmap="Blues")\
            .background_gradient(subset=["GOV/1000"], cmap="YlOrBr")\
            .background_gradient(subset=["Final Score"], cmap="Reds")\
            .format({c: "{:.3f}" for c in ["ENV/1000", "SOCIAL/1000", "GOV/1000", "Controversy", "Final Score"]})\
            .hide(axis="index")

        st.dataframe(norm_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">FinBERT Sentiment Analysis — Financial BERT Model</div>', unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([1.2, 1])

    with col_s1:
        # Sentiment bar chart
        if "avg_sentiment" in filtered_scores.columns:
            sent_sorted = filtered_scores.sort_values("avg_sentiment")

            fig5, ax5 = plt.subplots(figsize=(7, 5))
            sent_colors = [COLORS["High Risk"] if v < -0.4
                           else COLORS["Medium Risk"] if v < -0.2
                           else COLORS["Low Risk"]
                           for v in sent_sorted["avg_sentiment"]]

            bars5 = ax5.barh(sent_sorted["company"], sent_sorted["avg_sentiment"],
                             color=sent_colors, height=0.55, zorder=3)

            ax5.axvline(x=0, color="#475569", linewidth=1, linestyle="-", zorder=4)
            ax5.set_xlabel("Average Sentiment Score (-1=Negative, +1=Positive)")
            ax5.set_title("Company Sentiment — FinBERT Analysis", color="#dde3ed",
                          fontsize=9, fontweight="bold")
            ax5.grid(axis="x", zorder=0)
            ax5.spines[["top", "right", "left"]].set_visible(False)

            for bar, val in zip(bars5, sent_sorted["avg_sentiment"]):
                xpos = bar.get_width() - 0.02 if val < 0 else bar.get_width() + 0.01
                ax5.text(xpos, bar.get_y() + bar.get_height()/2,
                         f"{val:.4f}", va="center", fontsize=7,
                         color="#94a3b8", ha="right" if val < 0 else "left",
                         fontfamily="monospace")

            plt.tight_layout()
            st.pyplot(fig5, use_container_width=True)
            plt.close()

    with col_s2:
        st.markdown("<br>", unsafe_allow_html=True)

        if "avg_sentiment" in filtered_scores.columns:
            sent_display = filtered_scores[
                ["company", "avg_sentiment", "negative_articles",
                 "positive_articles", "neutral_articles"]
            ].sort_values("avg_sentiment").copy()
            sent_display.columns = ["Company", "Avg Sentiment", "Negative", "Positive", "Neutral"]

            st.dataframe(sent_display, use_container_width=True, hide_index=True, height=320)

        st.markdown("""
        <div class="warn-box">
            ⚠️ <b>Model Limitation:</b> FinBERT trained on general financial news. 
            ENV keywords (e.g. "net-zero") may read as positive business language. 
            Correlation: ENV score vs sentiment = +0.389
        </div>
        """, unsafe_allow_html=True)

    # Sentiment distribution
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Article-Level Sentiment Distribution</div>', unsafe_allow_html=True)

    if "sentiment_label" in articles_df.columns:
        sent_dist = articles_df["sentiment_label"].value_counts()

        fig6, ax6 = plt.subplots(1, 2, figsize=(12, 3.5))

        # Bar chart
        dist_colors = {"negative": COLORS["High Risk"],
                       "neutral":  COLORS["muted"],
                       "positive": COLORS["Low Risk"]}
        colors_dist = [dist_colors.get(l, "#475569") for l in sent_dist.index]
        ax6[0].bar(sent_dist.index, sent_dist.values, color=colors_dist,
                   width=0.5, zorder=3)
        ax6[0].set_title("Sentiment Label Distribution", color="#dde3ed",
                         fontsize=9, fontweight="bold")
        ax6[0].grid(axis="y", zorder=0)
        ax6[0].spines[["top", "right"]].set_visible(False)
        for i, (label, val) in enumerate(zip(sent_dist.index, sent_dist.values)):
            ax6[0].text(i, val + 0.5, str(val), ha="center",
                        fontsize=9, color="#dde3ed", fontfamily="monospace")

        # Score distribution scatter per company
        if "sentiment_score" in articles_df.columns:
            comp_colors_map = {
                "High Risk": COLORS["High Risk"],
                "Medium Risk": COLORS["Medium Risk"],
                "Low Risk": COLORS["Low Risk"]
            }
            merged = articles_df.merge(
                scores_df[["company", "risk_tier"]], on="company", how="left"
            )
            for tier, grp in merged.groupby("risk_tier"):
                ax6[1].scatter(
                    grp["company"], grp["sentiment_score"],
                    color=comp_colors_map.get(tier, "#475569"),
                    s=20, alpha=0.6, label=tier, zorder=3
                )
            ax6[1].axhline(y=0, color="#475569", linewidth=1, linestyle="--")
            ax6[1].set_title("Sentiment Score per Article by Company",
                             color="#dde3ed", fontsize=9, fontweight="bold")
            ax6[1].tick_params(axis="x", rotation=35)
            ax6[1].spines[["top", "right"]].set_visible(False)
            ax6[1].grid(axis="y", zorder=0)
            ax6[1].legend(facecolor="#0d1117", edgecolor="#1a2030",
                          labelcolor="#dde3ed", fontsize=7)

        plt.tight_layout()
        st.pyplot(fig6, use_container_width=True)
        plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: ARTICLE EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Article-Level Signal Explorer</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filter_company = st.selectbox(
            "Filter Company",
            ["All"] + sorted(articles_df["company"].unique().tolist())
        )
    with col_f2:
        filter_cat = st.selectbox(
            "ESG Category",
            ["All", "Environmental", "Social", "Governance"]
        )
    with col_f3:
        if "sentiment_label" in articles_df.columns:
            filter_sent = st.selectbox(
                "Sentiment",
                ["All", "negative", "neutral", "positive"]
            )
        else:
            filter_sent = "All"

    art_df = articles_df.copy()
    if filter_company != "All":
        art_df = art_df[art_df["company"] == filter_company]
    if filter_cat != "All" and "esg_category" in art_df.columns:
        art_df = art_df[art_df["esg_category"] == filter_cat]
    if filter_sent != "All" and "sentiment_label" in art_df.columns:
        art_df = art_df[art_df["sentiment_label"] == filter_sent]

    show_cols = ["company", "esg_category", "env_score", "social_score",
                 "gov_score", "sentiment_label", "sentiment_score", "url"]
    available_cols = [c for c in show_cols if c in art_df.columns]

    st.markdown(f"""
    <div class="info-box">
        📰 Showing <b>{len(art_df)}</b> articles matching filters
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        art_df[available_cols].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        height=350
    )

    # Article detail expander
    if len(art_df) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Article Deep Dive</div>', unsafe_allow_html=True)

        article_idx = st.selectbox(
            "Select article to inspect",
            options=range(min(len(art_df), 20)),
            format_func=lambda i: f"{art_df.iloc[i]['company']} — {str(art_df.iloc[i].get('url', ''))[:60]}..."
        )

        if article_idx is not None:
            row = art_df.iloc[article_idx]

            col_d1, col_d2, col_d3, col_d4 = st.columns(4)
            col_d1.metric("ENV Score",    int(row.get("env_score", 0)))
            col_d2.metric("SOCIAL Score", int(row.get("social_score", 0)))
            col_d3.metric("GOV Score",    int(row.get("gov_score", 0)))
            col_d4.metric("Sentiment",    f"{row.get('sentiment_score', 0):.4f}")

            with st.expander("📄 Article Text Preview (first 1000 chars)"):
                raw = str(row.get("raw_text", "No text available"))
                st.markdown(f"""
                <div style='background: #0d1117; border: 1px solid #1a2030; padding: 1rem;
                            font-family: Crimson Pro, Georgia, serif; font-size: 0.95rem;
                            color: #94a3b8; line-height: 1.7;'>
                    {raw[:1000]}...
                </div>
                """, unsafe_allow_html=True)

            if "url" in row:
                st.markdown(f"🔗 **Source:** [{row['url'][:80]}...]({row['url']})")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: METHODOLOGY
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<br>", unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.4rem; color: #dc2626; letter-spacing: 0.06em;'>
            SCORING FORMULA
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        ```
        ┌─────────────────────────────────────────┐
        │           FINAL SCORE FORMULA            │
        ├─────────────────────────────────────────┤
        │                                         │
        │  severity = (ENV × 0.5)                 │
        │           + (SOCIAL × 0.3)              │
        │           + (GOV × 0.2)                 │
        │                                         │
        │  volume   = log1p(article_count)        │
        │                                         │
        │  controversy = (severity × 0.7)         │
        │              + (volume × 0.3)            │
        │                                         │
        │  final = (controversy × 0.7)            │
        │        + (|avg_sentiment| × 0.3)        │
        │                                         │
        └─────────────────────────────────────────┘
        ```
        """)

        st.markdown("""
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.4rem; color: #dc2626; letter-spacing: 0.06em; margin-top: 1rem;'>
            WEIGHT RATIONALE
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        | Weight | Reason |
        |--------|--------|
        | ENV = 50% | Primary risk for Oil & Gas sector |
        | SOCIAL = 30% | Human impact and community issues |
        | GOV = 20% | Regulatory and legal exposure |
        | Severity × 70% | Keyword intensity most predictive |
        | Volume × 30% | Prevents hiding via single articles |
        | Sentiment × 30% | FinBERT adds tone signal |
        """)

    with col_m2:
        st.markdown("""
        <div style='font-family: Bebas Neue, sans-serif; font-size: 1.4rem; color: #dc2626; letter-spacing: 0.06em;'>
            PIPELINE STAGES
        </div>
        """, unsafe_allow_html=True)

        stages = [
            ("01", "INGESTION",    "Parse company,URL pairs → raw CSV"),
            ("02", "EXTRACTION",   "Scrape text via requests + BeautifulSoup"),
            ("03", "CLEANING",     "Filter short/invalid + verify company mention"),
            ("04", "ESG TAGGING",  "Keyword scoring → ENV / SOCIAL / GOV"),
            ("05", "SENTIMENT",    "FinBERT per-chunk analysis + averaging"),
            ("06", "AGGREGATION",  "Company-level score + ranking"),
            ("07", "VISUALIZATION","Matplotlib charts + Streamlit dashboard"),
        ]

        for num, name, desc in stages:
            st.markdown(f"""
            <div style='display: flex; gap: 1rem; align-items: flex-start;
                        padding: 0.6rem 0; border-bottom: 1px solid #1a2030;'>
                <div style='font-family: Bebas Neue, sans-serif; font-size: 1.4rem;
                            color: #dc2626; min-width: 2rem;'>{num}</div>
                <div>
                    <div style='font-family: JetBrains Mono, monospace; font-size: 0.72rem;
                                color: #dde3ed; letter-spacing: 0.1em;'>{name}</div>
                    <div style='font-size: 0.82rem; color: #64748b; margin-top: 0.1rem;
                                font-style: italic;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top: 1.5rem; font-family: Bebas Neue, sans-serif; font-size: 1.4rem; color: #dc2626; letter-spacing: 0.06em;'>
            MODEL VALIDATION
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        | Check | Result |
        |-------|--------|
        | Scraping success rate | 87% (86/99 URLs) |
        | Negative articles | 63% (51/81) |
        | FinBERT accuracy (est.) | ~75% on ESG text |
        | Top 5 negatives verified | ✅ All confirmed |
        | ENV-sentiment correlation | +0.389 (known bias) |
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(220,38,38,0.06); border: 1px solid rgba(220,38,38,0.2);
                padding: 1.2rem 1.5rem; font-family: JetBrains Mono, monospace;
                font-size: 0.72rem; color: #94a3b8; line-height: 2;'>
        ⚠️ <span style='color: #fca5a5; font-weight: bold;'>DISCLAIMER:</span> 
        This system is an internship-level prototype built for learning and demonstration purposes 
        using historical public data. It is NOT intended for live trading, investment decisions, 
        or production ESG reporting. Results should be interpreted as signals for analyst review only.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top: 1px solid #1a2030; padding-top: 1rem; 
            display: flex; justify-content: space-between;
            font-family: JetBrains Mono, monospace; font-size: 0.6rem; color: #334155;'>
    <div>ESG CONTROVERSY SIGNAL ENGINE · OIL & GAS NLP INTELLIGENCE</div>
    <div>POWERED BY FINBERT · BEAUTIFULSOUP4 · STREAMLIT</div>
    <div>INTERNSHIP PROTOTYPE · NOT FOR PRODUCTION USE</div>
</div>
""", unsafe_allow_html=True)