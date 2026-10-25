# Pakistan House Prices Analysis (2023)

**Devixo Solutions | AI/ML Internship Program | Task 01**
Python Programming, Data Analysis & Visualization

**Author:** Noor ul Aien
**Internship Domain:** AI/ML

## Project Objective
Perform a complete data analysis workflow on a real-world dataset: data loading, understanding, cleaning, exploratory analysis, statistical analysis, visualization, insights and an interactive Streamlit dashboard.

## Dataset
- **Name:** Pakistan House Prices - 2023
- **Source:** [Kaggle](https://www.kaggle.com/datasets/manjitbaishya001/house-prices-2023)
- **Raw size:** 99,499 rows, 9 columns
- **Cleaned size:** 43,340 rows, 8 columns (For Sale listings only)
- **Columns:** property_type, price_pkr, location, city, bathrooms, purpose, bedrooms, area_marla

## Technologies and Libraries
- Python 3, Google Colab, Jupyter Notebook
- Pandas, NumPy, Matplotlib, Seaborn
- Streamlit (dashboard), ReportLab (PDF report)

## Project Workflow
Dataset selection, data loading, data understanding, data cleaning, exploratory data analysis, statistical analysis, data visualization, insights and findings, conclusion, documentation, GitHub organization.

## Data Cleaning Summary
- Dropped the unnamed index column
- Removed 37,858 duplicate rows (about 38%)
- Renamed columns (price_pkr, bathrooms, area_marla) and corrected data types
- Removed invalid rows: area <= 0 (10), bedrooms = 0 (283), area > 100 Marla (41)
- Kept only "For Sale" listings because rent and sale prices are on different scales

## Major Findings
- Prices are right-skewed: mean 13.57M vs median 10.9M PKR
- Islamabad and Lahore are the most expensive cities; Faisalabad is the cheapest
- Area has the strongest correlation with price (0.61)
- Bathrooms and bedrooms are strongly related (0.83)
- Houses are 67% of listings and have a higher median price than flats
- 20 Marla (1 Kanal) is a very common plot size

## Visualizations
Histogram, bar chart, pie chart, scatter plot, line chart, box plot, correlation heatmap, count plot, pair plot and violin plot (see the `images` folder).

## Project Structure
```
Task_01_AI_ML/
├── dataset/      house_prices.csv, cleaned_house_prices.csv
├── notebook/     Task_01_Data_Analysis.ipynb
├── images/       visualizations, code and dashboard screenshots
├── report/       Task_01_Report.pdf, make_report.py
├── app/          app.py (Streamlit dashboard)
├── requirements.txt
└── README.md
```

## How to Run
1. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
2. Open `notebook/Task_01_Data_Analysis.ipynb` in Google Colab or Jupyter Notebook.
3. Run the Streamlit dashboard:
   ```
   cd app
   streamlit run app.py
   ```
4. Generate the PDF report (optional):
   ```
   cd report
   python make_report.py
   ```

## Screenshots
### Dashboard
![Dashboard Overview](images/dashboard_01_overview.png)

### Visualizations
![Histogram](images/visualization_01_histogram_price.png)
![Correlation Heatmap](images/visualization_07_heatmap_correlation.png)
![Violin Plot](images/visualization_10_violin_property_price.png)

## Author
Noor ul Aien
GitHub: [shanaya3016](https://github.com/shanaya3016)