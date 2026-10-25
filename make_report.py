from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

# ------------------------------------------------------------------
# Details
# ------------------------------------------------------------------
NAME = "Noor ul Aien"
DOMAIN = "AI/ML"
SUBMISSION_DATE = "October 25, 2026"
GITHUB_USER = "shanaya3016"
REPO_LINK = f"https://github.com/{GITHUB_USER}/Task_01_AI_ML"

BASE = Path(__file__).resolve().parent.parent
IMG = BASE / "images"
OUT = BASE / "report" / "Task_01_Report.pdf"

GOLD = colors.HexColor("#b7791f")
DARK = colors.HexColor("#3b2a14")

# ------------------------------------------------------------------
# Styles
# ------------------------------------------------------------------
ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=10.5, leading=15, spaceAfter=6)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=16, textColor=DARK, spaceBefore=10, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12.5, textColor=GOLD, spaceBefore=8, spaceAfter=4)
cap = ParagraphStyle("cap", parent=body, fontSize=9, textColor=colors.grey, alignment=1)
center = ParagraphStyle("center", parent=body, alignment=1, fontSize=12, leading=18)
title_big = ParagraphStyle("tb", parent=ss["Title"], fontSize=26, textColor=DARK, leading=32)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=12, spaceAfter=0)
cell_h = ParagraphStyle("cellh", parent=cell, textColor=colors.white, fontName="Helvetica-Bold")
cell_b = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")

story = []


def P(text, style=body):
    story.append(Paragraph(text, style))


def bullets(items):
    for t in items:
        story.append(Paragraph(t, body, bulletText="•"))


def table(data, widths=None, header=True):
    wrapped = []
    for r, row in enumerate(data):
        if header and r == 0:
            style = cell_h
        else:
            style = cell
        wrapped.append([Paragraph(str(c), style) for c in row])
    t = Table(wrapped, colWidths=widths, repeatRows=1 if header else 0)
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9c79a")),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, colors.HexColor("#fdf8ec")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), GOLD))
    t.setStyle(TableStyle(cmds))
    story.append(t)
    story.append(Spacer(1, 8))


def picture(filename, caption, max_w=16 * cm, max_h=12 * cm):
    path = IMG / filename
    if not path.exists():
        P(f"<i>[Missing image: {filename}. Save it in the images folder and run the script again.]</i>", cap)
        print("MISSING:", filename)
        return
    w, h = PILImage.open(path).size
    scale = min(max_w / w, max_h / h)
    story.append(KeepTogether([
        Image(str(path), width=w * scale, height=h * scale),
        Spacer(1, 3),
        Paragraph(caption, cap),
        Spacer(1, 8),
    ]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Devixo Solutions | AI/ML Internship Program | Task 01")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


# ------------------------------------------------------------------
# Title page
# ------------------------------------------------------------------
story.append(Spacer(1, 3 * cm))
P("DEVIXO SOLUTIONS", ParagraphStyle("c1", parent=center, fontSize=20, textColor=GOLD))
P("AI/ML Internship Program", center)
story.append(Spacer(1, 1.2 * cm))
P("TASK 01", ParagraphStyle("c2", parent=center, fontSize=16))
P("Python Programming, Data Analysis &amp; Visualization", title_big)
story.append(Spacer(1, 0.6 * cm))
P("Pakistan House Prices Analysis (2023)", center)
story.append(Spacer(1, 2.5 * cm))
table([
    ["Student Name", NAME],
    ["Internship Domain", DOMAIN],
    ["Submission Date", SUBMISSION_DATE],
    ["GitHub", REPO_LINK],
], widths=[5 * cm, 11 * cm])
story.append(PageBreak())

# ------------------------------------------------------------------
# 1-6
# ------------------------------------------------------------------
P("1. Introduction", h1)
P("This report documents Task 01 of the Devixo Solutions AI/ML Internship Program. The task covers a complete "
  "data analysis workflow in Python: loading a real-world dataset, understanding its structure, cleaning and "
  "preprocessing it, performing exploratory and statistical analysis, creating visualizations and extracting "
  "insights. An optional interactive Streamlit dashboard was also built as a bonus.")

P("2. Objective", h1)
P("The objective is to build practical skills in Python, Pandas, NumPy, Matplotlib and Seaborn, and to show the "
  "ability to clean data, analyse it statistically, visualise it and explain the findings clearly.")

P("3. Dataset Name", h1)
P("Pakistan House Prices - 2023 (file: <b>house_prices.csv</b>)")

P("4. Dataset Source", h1)
P("Kaggle: https://www.kaggle.com/datasets/manjitbaishya001/house-prices-2023")

P("5. Dataset Description", h1)
P("The dataset contains property listings from major Pakistani cities, including the property type, location, "
  "city, price, number of bedrooms and bathrooms, area in Marla and the purpose of the listing (For Sale or For Rent). "
  "It mixes numerical and categorical variables, which makes it suitable for statistical analysis and visualization.")

P("6. Dataset Size", h1)
table([
    ["Stage", "Rows", "Columns"],
    ["Raw dataset", "99,499", "9"],
    ["After removing the index column and duplicates", "61,641", "8"],
    ["Final cleaned dataset (For Sale only)", "43,340", "8"],
], widths=[9 * cm, 3.5 * cm, 3.5 * cm])

# ------------------------------------------------------------------
# 7
# ------------------------------------------------------------------
P("7. Features / Columns Description", h1)
table([
    ["Column", "Type", "Description"],
    ["property_type", "Categorical", "House, Flat, Upper Portion, Lower Portion, Penthouse, Room, Farm House"],
    ["price_pkr", "Numerical", "Listing price in Pakistani Rupees (renamed from price)"],
    ["location", "Categorical", "Area or society of the property (e.g. DHA Defence)"],
    ["city", "Categorical", "Karachi, Lahore, Islamabad, Rawalpindi, Faisalabad"],
    ["bathrooms", "Numerical", "Number of bathrooms (renamed from baths)"],
    ["purpose", "Categorical", "For Sale or For Rent"],
    ["bedrooms", "Numerical", "Number of bedrooms"],
    ["area_marla", "Numerical", "Property area in Marla (renamed from Area_in_Marla)"],
], widths=[3.2 * cm, 2.6 * cm, 10.2 * cm])
P("The dataset has no date or time column. The unnamed index column (Unnamed: 0) was dropped.")

# ------------------------------------------------------------------
# 8-9
# ------------------------------------------------------------------
P("8. Methodology", h1)
P("The work followed the workflow given in the task document:")
bullets([
    "Dataset selection and loading",
    "Data understanding (head, tail, sample, info, shape, column types)",
    "Data cleaning and preprocessing",
    "Exploratory data analysis and statistical analysis",
    "Data visualization with interpretation of every chart",
    "Insights, conclusion, documentation and GitHub organization",
])
P("Tools used: Python 3, Google Colab, Pandas, NumPy, Matplotlib, Seaborn and Streamlit.")

P("9. Data Loading", h1)
P("The libraries were imported and the CSV file was loaded into a Pandas DataFrame using <i>pd.read_csv()</i>. "
  "The first 5 rows, last 5 rows and a random sample of 5 rows were displayed, followed by df.info(), the column "
  "names, data types, missing values and the dataset shape (99,499 rows and 9 columns).")
P("Column types: numerical columns were price, bathrooms, bedrooms and area. Categorical columns were "
  "property_type, location, city and purpose. No date/time columns were found. Identifying column types is "
  "important because numerical columns are used for statistics and correlation, while categorical columns are used "
  "for grouping and counting.")

# ------------------------------------------------------------------
# 10
# ------------------------------------------------------------------
P("10. Data Cleaning", h1)
table([
    ["Step", "Finding", "Action"],
    ["Missing values", "0 in every column", "No imputation needed"],
    ["Index column", "Unnamed: 0 carried no information", "Dropped"],
    ["Duplicates", "37,858 duplicate rows (about 38%)", "Removed and verified (0 remaining)"],
    ["Column names", "Inconsistent names", "Renamed to price_pkr, bathrooms, area_marla"],
    ["Data types", "Text columns stored as object", "property_type, city, purpose converted to category"],
    ["Area &lt;= 0", "10 rows", "Removed (zero area is impossible)"],
    ["Bedrooms = 0", "283 rows", "Removed (not comparable)"],
    ["Area &gt; 100 Marla", "41 rows", "Removed as extreme outliers"],
    ["Rent vs Sale", "Prices on completely different scales", "Rent rows (17,967) set aside; analysis on For Sale only"],
], widths=[3 * cm, 6 * cm, 7 * cm])
P("After cleaning, the dataset was verified: 0 missing values, 0 duplicates, correct data types and a final shape "
  "of 43,340 rows and 8 columns.")

# ------------------------------------------------------------------
# 11-12
# ------------------------------------------------------------------
P("11. Exploratory Data Analysis", h1)
bullets([
    "<b>Most common property type:</b> House (29,041 listings).",
    "<b>Most common city:</b> Karachi (15,955 listings), followed by Lahore (14,483).",
    "<b>Most common location:</b> DHA Defence (2,528 listings).",
    "<b>Price range:</b> from about PKR 16,000 to PKR 44.9 million.",
    "<b>Outliers:</b> many high-price outliers exist in every city and a few very large plots (60 to 100 Marla).",
    "<b>Related variables:</b> price is most related to area, then bathrooms and bedrooms.",
])
table([
    ["City", "Mean price (PKR)", "Median price (PKR)", "Listings"],
    ["Islamabad", "14,635,707", "12,500,000", "6,598"],
    ["Lahore", "14,608,297", "12,000,000", "14,483"],
    ["Karachi", "12,893,316", "9,500,000", "15,955"],
    ["Rawalpindi", "12,114,902", "9,500,000", "4,779"],
    ["Faisalabad", "10,678,076", "8,100,000", "1,525"],
], widths=[3.5 * cm, 4.2 * cm, 4.5 * cm, 3.8 * cm])

P("12. Statistical Analysis", h1)
table([
    ["Measure", "Value", "Meaning"],
    ["Mean price", "PKR 13,567,891", "Average price, pulled up by luxury listings"],
    ["Median price", "PKR 10,900,000", "Typical price, not affected by outliers"],
    ["Std deviation", "PKR 9,852,649", "Prices vary widely around the mean"],
    ["Skewness", "1.12", "Right-skewed distribution"],
    ["Mode (type / city / location)", "House / Karachi / DHA Defence", "Most frequent categories"],
], widths=[4.5 * cm, 4.5 * cm, 7 * cm])
P("<b>Mean vs median:</b> the mean (13.57 million) is higher than the median (10.9 million). Because a few "
  "very expensive properties pull the mean upward, the median is the better measure of a typical price.")
P("<b>Correlation analysis:</b>")
table([
    ["Pair", "Correlation", "Strength"],
    ["price and area", "0.61", "Strongest with price"],
    ["price and bathrooms", "0.58", "Moderate"],
    ["price and bedrooms", "0.53", "Moderate"],
    ["bathrooms and bedrooms", "0.83", "Very strong"],
    ["bathrooms and area", "0.42", "Moderate"],
    ["bedrooms and area", "0.38", "Weak to moderate"],
], widths=[6 * cm, 4 * cm, 6 * cm])
P("All correlations are positive and none (except with itself) is close to 1, so price depends on several factors "
  "together, including city and location.")
story.append(PageBreak())

# ------------------------------------------------------------------
# 13 Visualizations
# ------------------------------------------------------------------
P("13. Data Visualizations", h1)

viz = [
    ("visualization_01_histogram_price.png", "Visualization 1: Histogram of Price",
     "Most listings are priced between about 3 and 10 million PKR, with a long tail up to about 45 million. "
     "The distribution is right-skewed (1.12), which explains why the mean is higher than the median."),
    ("visualization_02_bar_city_price.png", "Visualization 2: Bar Chart - Average Price by City",
     "Islamabad and Lahore (about 14.6 million each) are the most expensive, followed by Karachi and Rawalpindi. "
     "Faisalabad is the cheapest (10.7 million). City is an important pricing factor."),
    ("visualization_03_pie_property_type.png", "Visualization 3: Pie Chart - Property Type Share",
     "Houses make up about two thirds of listings (67%) and Flats about 28%. All other types together are a small "
     "share, so averages mostly describe houses and flats."),
    ("visualization_04_scatter_area_price.png", "Visualization 4: Scatter Plot - Area vs Price",
     "Within the main range (below 20 Marla) price rises with area. A vertical line at exactly 20 Marla (1 Kanal) "
     "shows a very common plot size. Above 40 Marla there are few listings and the relationship is scattered, so area "
     "alone cannot predict price."),
    ("visualization_05_line_bedrooms_price.png", "Visualization 5: Line Chart - Average Price by Bedrooms",
     "The dataset has no date column, so the trend is shown over bedrooms. Average price rises steadily from about "
     "4.5 million (1 bedroom) to about 22 million (6 bedrooms), with a slightly gentler slope after 5."),
    ("visualization_06_box_city_price.png", "Visualization 6: Box Plot - Price by City",
     "Islamabad and Lahore have the highest medians and Faisalabad the lowest. Every city has many high-price "
     "outliers, so the median is more reliable than the mean for comparing cities."),
    ("visualization_07_heatmap_correlation.png", "Visualization 7: Correlation Heatmap",
     "Bathrooms and bedrooms are the most strongly related (0.83). Price is most related to area (0.61). All values "
     "are positive. The overlap between bathrooms and bedrooms can cause multicollinearity in future ML models."),
    ("visualization_08_countplot_city.png", "Visualization 8: Count Plot - Listings by City",
     "Karachi (about 16,000) and Lahore (about 14,500) together make up about 70% of the data. Faisalabad has few "
     "listings (about 1,500), so its average is less reliable."),
    ("visualization_09_pairplot.png", "Visualization 9: Pair Plot",
     "Price and area are right-skewed. Bedrooms and bathrooms take whole numbers, forming lines of dots. A few very "
     "large plots stand apart. Skewed variables may need a log transform before machine learning."),
    ("visualization_10_violin_property_price.png", "Visualization 10: Violin Plot - Price by Property Type",
     "Houses have the highest median (about 12 to 13 million) and the widest spread. Flats have the lowest median "
     "(about 7 million). All types have long upper tails, so property type is an important price factor."),
]
for fname, title, text in viz:
    P(title, h2)
    picture(fname, title, max_w=14.5 * cm, max_h=9.5 * cm)
    P("<b>Interpretation:</b> " + text)

story.append(PageBreak())

# ------------------------------------------------------------------
# 14-16 Screenshots
# ------------------------------------------------------------------
P("14. Code Screenshots", h1)
picture("code_1_load.png", "Libraries import and dataset loading")
picture("code_3_cleaning.png", "Data cleaning: duplicate records")
picture("code_4_invalid_values.png", "Data cleaning: invalid values")
picture("code_5_descriptive_statistics.png", "Descriptive Statistical analysis code")
picture("code_6_correlation_analysis.png", "Correlation analysis code")
P("15. Output Screenshots", h1)
picture("code_2_info.png", "Dataset information, shape and missing values")
P("The cleaned dataset was verified with 0 missing values, 0 duplicates and a shape of (43340, 8).")

P("16. Graph Screenshots and Streamlit Dashboard", h1)
P("All 10 graphs are shown in Section 13. The optional Streamlit dashboard uses the same charts with interactive "
  "filters (city, property type, bedrooms, price and area), KPI cards, summary statistics, a correlation heatmap, "
  "key insights and a CSV download button.")
picture("dashboard_1_overview.png", "Dashboard: Overview tab")
picture("dashboard_2_price.png", "Dashboard: Price Analysis tab")
picture("dashboard_3_relationship.png", "Dashboard: Relationships tab")
picture("dashboard_4_data.png", "Dashboard: Data and Stats tab")
picture("dashboard_5_insights.png", "Dashboard: Insights tab")
story.append(PageBreak())

# ------------------------------------------------------------------
# 17-20
# ------------------------------------------------------------------
P("17. Major Findings", h1)
bullets([
    "The raw data had about 38% duplicate rows and mixed rent and sale prices, which would have distorted the analysis.",
    "Sale prices are right-skewed: mean 13.57 million versus median 10.9 million PKR.",
    "Islamabad and Lahore are the most expensive cities; Faisalabad is the most affordable.",
    "Area has the strongest correlation with price (0.61); bathrooms and bedrooms are strongly related (0.83).",
    "Houses are 67% of listings and have a higher median price than flats.",
])

P("18. Insights", h1)
insights = [
    "<b>Houses dominate the market:</b> houses are 67% of sale listings (29,041), followed by flats at 28%.",
    "<b>Prices are right-skewed:</b> mean 13.57M versus median 10.9M PKR (skewness 1.12) because a few luxury properties pull the average up.",
    "<b>Islamabad and Lahore are the most expensive cities:</b> both average about 14.6M PKR, while Faisalabad is the cheapest at about 10.7M.",
    "<b>Karachi has the most listings:</b> 15,955 (about 37%), with Lahore second at 14,483.",
    "<b>Area is the strongest numeric driver of price:</b> correlation 0.61.",
    "<b>Bathrooms and bedrooms are strongly related:</b> correlation 0.83, the highest in the dataset, which suggests overlapping information.",
    "<b>Price rises steadily with bedrooms:</b> from about 4.5M PKR for 1 bedroom to about 22M PKR for 6 bedrooms.",
    "<b>Prices vary widely:</b> the standard deviation (9.85M PKR) is large compared with the mean.",
    "<b>Outliers exist in every city:</b> the box plot shows many high-price outliers, so the median is more reliable than the mean.",
    "<b>20 Marla (1 Kanal) is a very common plot size:</b> the scatter plot shows a vertical line of listings at exactly 20 Marla.",
    "<b>Data quality problems were found:</b> about 38% of raw records (37,858) were duplicates and rent and sale prices were mixed.",
    "<b>Houses are priced higher than flats:</b> the violin plot shows a higher median price for houses.",
]
for i, t in enumerate(insights, 1):
    story.append(Paragraph(f"{i}. {t}", body))

P("19. Conclusion", h1)
P("In this project I analysed the Pakistan House Prices 2023 dataset from Kaggle. The raw data had 99,499 rows. "
  "During cleaning I removed the unnamed index column, 37,858 duplicate records and rows with invalid values "
  "(zero area, zero bedrooms and extreme areas above 100 Marla). I also renamed columns, corrected data types and "
  "kept only For Sale listings because rent and sale prices are on completely different scales. The final dataset has "
  "43,340 rows and 8 columns. I then performed descriptive statistics, correlation analysis and created 10 "
  "visualizations, along with an interactive Streamlit dashboard.")
P("The most important findings are that prices are right-skewed (mean 13.57M versus median 10.9M PKR), Islamabad and "
  "Lahore are the most expensive cities, and area has the strongest relationship with price (0.61). Houses make up "
  "two thirds of listings and cost more than flats. From this project I learned the complete data analysis workflow: "
  "cleaning real data, choosing suitable statistics, creating clear charts and interpreting them. The analysis can help "
  "buyers compare cities and property types, and it prepares the ground for future machine learning tasks such as house "
  "price prediction.")

P("20. GitHub Repository Link", h1)
P(f'<link href="{REPO_LINK}" color="blue">{REPO_LINK}</link>')

# ------------------------------------------------------------------
doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm, title="Task 01 Report", author=NAME,
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Report saved to:", OUT)