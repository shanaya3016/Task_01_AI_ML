from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# ------------------------------------------------------------------
# Page setup
# ------------------------------------------------------------------
st.set_page_config(page_title="Pakistan House Prices Dashboard", page_icon="🏠", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px;}
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent !important;}
.stDeployButton, [data-testid="stToolbar"] {display: none !important;}

/* Sand Gold theme */
.stApp {background: linear-gradient(160deg, #fdf8ec 0%, #f6ecd2 100%) !important;}
section[data-testid="stSidebar"] {background: #f1e2bd !important; border-right: 1px solid #e0cc9a;}
span[data-baseweb="tag"] {background-color: #b7791f !important; color: white !important;}

/* Gold tabs and sliders */
button[data-baseweb="tab"] {font-weight: 600; font-size: 1rem;}
button[data-baseweb="tab"][aria-selected="true"] {color: #b7791f !important;}
div[data-baseweb="tab-highlight"] {background-color: #b7791f !important;}
div[data-baseweb="slider"] div[role="slider"] {background-color: #b7791f !important;}
div[data-baseweb="slider"] > div > div > div {background: #b7791f !important;}
div[data-testid="stSliderThumbValue"],
div[data-testid="stTickBarMin"],
div[data-testid="stTickBarMax"] {color: #8a6d3b !important;}

.hero {
    background: linear-gradient(115deg, #3b2a14 0%, #6b4a1e 55%, #b7791f 100%);
    padding: 2rem 2.4rem; border-radius: 22px; color: white; margin-bottom: 1.2rem;
    box-shadow: 0 14px 34px rgba(59,42,20,0.30); position: relative; overflow: hidden;
}
.hero:after {
    content: ""; position: absolute; right: -60px; top: -60px; width: 240px; height: 240px;
    border-radius: 50%; background: radial-gradient(circle, rgba(253,230,138,0.55), transparent 70%);
}
.hero h1 {margin: 0; font-size: 2.1rem; font-weight: 800; color: white;}
.hero p {margin: .45rem 0 0 0; opacity: .92; font-size: 1rem;}
.badge {
    display: inline-block; margin-top: .9rem; padding: .25rem .8rem; border-radius: 999px;
    background: rgba(253,230,138,0.18); border: 1px solid #fde68a; color: #fde68a;
    font-size: .78rem; font-weight: 600; letter-spacing: .04em;
}

.kpi {
    background: #fffdf6; border-radius: 16px; padding: 1rem 1.2rem;
    border: 1px solid #ecdcae; border-top: 4px solid #b7791f;
    box-shadow: 0 4px 14px rgba(120,84,20,0.10); transition: all .2s ease;
}
.kpi:hover {transform: translateY(-4px); box-shadow: 0 12px 26px rgba(120,84,20,0.20);}
.kpi-label {font-size: .74rem; text-transform: uppercase; letter-spacing: .08em; color: #8a6d3b;}
.kpi-value {font-size: 1.7rem; font-weight: 800; color: #3b2a14; margin-top: .1rem;}
.kpi-sub {font-size: .78rem; color: #b7791f; font-weight: 600;}

.section-title {font-size: 1.2rem; font-weight: 700; color: #3b2a14; margin: .6rem 0 .3rem 0;}
.insight {
    background: #fffdf6; border-radius: 14px; padding: .95rem 1.15rem; margin-bottom: .75rem;
    border: 1px solid #ecdcae; border-left: 5px solid #b7791f;
    box-shadow: 0 3px 10px rgba(120,84,20,0.08); color: #3b2a14;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fffdf6 !important; border-color: #ecdcae !important; border-radius: 16px;
    box-shadow: 0 4px 14px rgba(120,84,20,0.08);
}
</style>
""",
    unsafe_allow_html=True,
)

# Same chart style as the notebook
sns.set_style("whitegrid")


# ------------------------------------------------------------------
# Data
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    base = Path(__file__).resolve().parent.parent
    return pd.read_csv(base / "dataset" / "cleaned_house_prices.csv")


df = load_data()
NUM_COLS = ["price_pkr", "bathrooms", "bedrooms", "area_marla"]
MAIN_TYPES = ["House", "Flat", "Upper Portion", "Lower Portion"]


def kpi(label, value, sub=""):
    return (
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'
    )


def show(fig):
    st.pyplot(fig, use_container_width=True, clear_figure=True)
    plt.close(fig)


# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.markdown("## 🎛️ Filters")
all_cities = sorted(df["city"].unique())
cities = st.sidebar.multiselect("City", all_cities, default=all_cities)

all_types = sorted(df["property_type"].unique())
default_types = [t for t in MAIN_TYPES if t in all_types]
types = st.sidebar.multiselect("Property Type", all_types, default=default_types)

bmin, bmax = int(df["bedrooms"].min()), int(df["bedrooms"].max())
beds = st.sidebar.slider("Bedrooms", bmin, bmax, (bmin, bmax))

pmax = float(df["price_pkr"].max() / 1e6)
price_range = st.sidebar.slider("Price (Million PKR)", 0.0, pmax, (0.0, pmax), step=0.5)

amax = float(df["area_marla"].max())
area_range = st.sidebar.slider("Area (Marla)", 0.0, amax, (0.0, amax), step=0.5)

fdf = df[
    df["city"].isin(cities)
    & df["property_type"].isin(types)
    & df["bedrooms"].between(*beds)
    & (df["price_pkr"] / 1e6).between(*price_range)
    & df["area_marla"].between(*area_range)
].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** listings")
st.sidebar.caption("Devixo Solutions · AI/ML Internship · Task 01")

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <h1>🏠 Pakistan House Prices Dashboard</h1>
  <p>Interactive analysis of property listings for sale across 5 major cities</p>
  <span class="badge">FOR SALE LISTINGS · 2023 DATA</span>
</div>
""",
    unsafe_allow_html=True,
)

if fdf.empty:
    st.warning("No listings match the selected filters. Please widen the filters in the sidebar.")
    st.stop()

fdf["price_m"] = fdf["price_pkr"] / 1e6

# ------------------------------------------------------------------
# KPI cards
# ------------------------------------------------------------------
top_city = fdf.groupby("city")["price_m"].mean().idxmax()
k1, k2, k3, k4, k5 = st.columns(5)
k1.markdown(kpi("Total Records", f"{len(fdf):,}", f"{df.shape[1]} columns"), unsafe_allow_html=True)
k2.markdown(kpi("Average Price", f"{fdf['price_m'].mean():.1f} M", "PKR"), unsafe_allow_html=True)
k3.markdown(kpi("Median Price", f"{fdf['price_m'].median():.1f} M", "PKR"), unsafe_allow_html=True)
k4.markdown(kpi("Avg Area", f"{fdf['area_marla'].mean():.1f}", "Marla"), unsafe_allow_html=True)
k5.markdown(kpi("Priciest City", top_city, "highest average price"), unsafe_allow_html=True)
st.write("")

# ------------------------------------------------------------------
# Tabs (charts are the same as in the notebook)
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "💰 Price Analysis", "🔗 Relationships", "🗂️ Data & Stats", "💡 Insights"]
)

# ---------------- Overview (4 charts in one row) ----------------
with tab1:
    c1, c2, c3, c4 = st.columns(4)

    with c1, st.container(border=True):
        fig, ax = plt.subplots(figsize=(5, 4.2))
        sns.histplot(fdf["price_m"], bins=50, kde=True, color="steelblue", ax=ax)
        ax.set_title("Distribution of House Prices", fontsize=11)
        ax.set_xlabel("Price (Million PKR)", fontsize=9)
        ax.set_ylabel("Number of Listings", fontsize=9)
        show(fig)

    with c2, st.container(border=True):
        city_avg = fdf.groupby("city")["price_m"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(5, 4.2))
        sns.barplot(x=city_avg.index.astype(str), y=city_avg.values, palette="viridis", ax=ax)
        ax.set_title("Average Price by City", fontsize=11)
        ax.set_xlabel("City", fontsize=9)
        ax.set_ylabel("Avg Price (Million PKR)", fontsize=9)
        ax.tick_params(axis="x", labelsize=7, rotation=20)
        show(fig)

    with c3, st.container(border=True):
        counts = fdf["property_type"].astype(str).value_counts()
        share = counts / counts.sum()
        main = counts[share >= 0.04]
        other = counts[share < 0.04].sum()
        pie_data = pd.concat([main, pd.Series({"Other": other})]) if other > 0 else main
        total = pie_data.sum()
        fig, ax = plt.subplots(figsize=(5, 4.2))
        wedges, _, _ = ax.pie(
            pie_data, labels=None, startangle=90,
            autopct=lambda p: f"{p:.1f}%" if p >= 4 else "",
            colors=sns.color_palette("pastel", len(pie_data)),
            pctdistance=0.7, wedgeprops={"edgecolor": "white"},
            textprops={"fontsize": 8},
        )
        legend_labels = [f"{n} ({v / total * 100:.1f}%)" for n, v in pie_data.items()]
        ax.legend(wedges, legend_labels, loc="lower center",
                  bbox_to_anchor=(0.5, -0.02), frameon=False, fontsize=7, ncol=1)
        ax.set_title("Share by Property Type", fontsize=11)
        fig.subplots_adjust(bottom=0.25)
        show(fig)

    with c4, st.container(border=True):
        fig, ax = plt.subplots(figsize=(5, 4.2))
        sns.countplot(data=fdf, x=fdf["city"].astype(str),
                      order=fdf["city"].astype(str).value_counts().index,
                      palette="mako", ax=ax)
        ax.set_title("Listings by City", fontsize=11)
        ax.set_xlabel("City", fontsize=9)
        ax.set_ylabel("Number of Listings", fontsize=9)
        ax.tick_params(axis="x", labelsize=7, rotation=20)
        show(fig)

# ---------------- Price analysis ----------------
with tab2:
    c1, c2, c3 = st.columns(3)
    with c1, st.container(border=True):
        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.boxplot(data=fdf, x=fdf["city"].astype(str), y="price_m", palette="Set2", ax=ax)
        ax.set_title("Price Distribution by City", fontsize=12)
        ax.set_xlabel("City")
        ax.set_ylabel("Price (Million PKR)")
        ax.tick_params(axis="x", labelsize=8, rotation=20)
        show(fig)
    with c2, st.container(border=True):
        vt = fdf[fdf["property_type"].astype(str).isin(MAIN_TYPES)].copy()
        vt["property_type"] = vt["property_type"].astype(str)
        fig, ax = plt.subplots(figsize=(6, 4.5))
        if vt.empty:
            ax.text(0.5, 0.5, "No data for the selected filters", ha="center")
        else:
            sns.violinplot(data=vt, x="property_type", y="price_m", palette="muted", ax=ax)
        ax.set_title("Price Distribution by Property Type", fontsize=12)
        ax.set_xlabel("Property Type")
        ax.set_ylabel("Price (Million PKR)")
        ax.tick_params(axis="x", labelsize=8, rotation=20)
        show(fig)
    with c3, st.container(border=True):
        bed_avg = fdf.groupby("bedrooms")["price_m"].mean()
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.plot(bed_avg.index, bed_avg.values, marker="o", linewidth=2, color="darkgreen")
        ax.set_title("Average Price by Number of Bedrooms", fontsize=12)
        ax.set_xlabel("Number of Bedrooms")
        ax.set_ylabel("Average Price (Million PKR)")
        ax.grid(True)
        show(fig)

# ---------------- Relationships ----------------
with tab3:
    c1, c2 = st.columns([3, 2])
    with c1, st.container(border=True):
        sample = fdf.sample(min(3000, len(fdf)), random_state=42).copy()
        sample["city"] = sample["city"].astype(str)
        fig, ax = plt.subplots(figsize=(9, 5.5))
        sns.scatterplot(data=sample, x="area_marla", y="price_m", hue="city", alpha=0.6, ax=ax)
        ax.set_title("Property Area vs Price", fontsize=14)
        ax.set_xlabel("Area (Marla)")
        ax.set_ylabel("Price (Million PKR)")
        show(fig)
    with c2, st.container(border=True):
        fig, ax = plt.subplots(figsize=(6, 5.5))
        sns.heatmap(fdf[NUM_COLS].corr(), annot=True, cmap="coolwarm", fmt=".2f",
                    linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap of Numeric Features", fontsize=13)
        show(fig)

    st.info(
        "**How to read this:** the closer a correlation is to +1, the more strongly the two "
        "features rise together. Area has the strongest link with price, while bathrooms and "
        "bedrooms are very strongly related to each other."
    )

    if st.checkbox("Show pair plot (takes a few seconds)"):
        with st.container(border=True):
            pair_sample = fdf[NUM_COLS].sample(min(1000, len(fdf)), random_state=42)
            g = sns.pairplot(pair_sample, diag_kind="kde")
            g.fig.suptitle("Pair Plot of Numeric Features", y=1.02, fontsize=14)
            st.pyplot(g.fig, use_container_width=True)
            plt.close(g.fig)

# ---------------- Data & stats ----------------
with tab4:
    st.markdown('<div class="section-title">Summary Statistics</div>', unsafe_allow_html=True)
    st.dataframe(fdf[NUM_COLS].describe().round(2), use_container_width=True)

    st.markdown('<div class="section-title">Filtered Data (first 500 rows)</div>', unsafe_allow_html=True)
    st.dataframe(fdf.drop(columns=["price_m"]).head(500), use_container_width=True, height=380)

    st.download_button(
        "⬇️ Download filtered data (CSV)",
        fdf.drop(columns=["price_m"]).to_csv(index=False).encode("utf-8"),
        file_name="filtered_house_prices.csv",
        mime="text/csv",
    )

# ---------------- Insights ----------------
with tab5:
    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
    insights = [
        "<b>Houses dominate:</b> about 67% of sale listings are houses, followed by flats at 28%.",
        "<b>Right-skewed prices:</b> the mean price is higher than the median, so the median is a better measure of a typical property.",
        "<b>City matters:</b> Islamabad and Lahore have the highest average prices, while Faisalabad is the most affordable.",
        "<b>Area drives price:</b> area has the strongest correlation with price (0.61).",
        "<b>Overlapping features:</b> bathrooms and bedrooms are strongly related (0.83), which matters for future ML models.",
        "<b>Steady growth:</b> average price rises steadily from 1 to 6 bedrooms.",
    ]
    cols = st.columns(2)
    for i, text in enumerate(insights):
        cols[i % 2].markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

st.caption("Built with Streamlit · Devixo Solutions AI/ML Internship · Task 01")