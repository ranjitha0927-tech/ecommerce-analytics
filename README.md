# E-Commerce Customer, Sales & Profitability Analytics

An end-to-end business intelligence portfolio project built from the existing cleaned e-commerce transaction dataset. It combines a pandas cleaning and analysis workflow, SQLite queries, saved Matplotlib charts, and a multi-page interactive Streamlit dashboard.

## Business problem

An e-commerce team needs a clear view of what drives sales and profit, which customers and cities contribute most, and how discounts, payment choices and order outcomes relate to performance.

## Objectives

- Clean and validate transaction data using Python and pandas.
- Analyze customers, categories, cities, discounts, payment methods and order outcomes.
- Store the cleaned records in SQLite and answer business questions with SQL.
- Present interactive, filterable metrics and charts in a portfolio-ready dashboard.

## Dataset

The project includes `data/raw_data.csv`, `data/raw_data_backup.csv`, and `data/cleaned_data.csv`. Each row represents a transaction/product line and includes order/customer IDs, customer name, age, gender, city, category, quantity, unit price, discount, sales, cost, profit, payment method and order status. Monetary values are displayed in INR.

There is no transaction date, geographic coordinate, product SKU, or customer contact/identity field. Trend charts, accurate mapping, and individual identity verification therefore need additional source data. Customer names in the generated sample are not unique identifiers; customer analysis uses Customer_ID.

## Data cleaning

`data/clean_data.py` retains the original cleaning steps: remove duplicate rows, standardize category capitalization, fill missing names/cities with `Unknown`, and fill missing ages with the dataset mean. The Business Insights page reports record counts, missing values remaining, and duplicates removed.

## SQL analysis

`data/sql/ecommerce_analysis.sql` contains the existing SQL analysis queries. `data/sql/setup_database.py` loads the cleaned CSV into the SQLite `sales` table. The dashboard also reads a category summary from this database; its interactive views use the cleaned CSV so the global filters remain consistent.

## Python analysis and charts

`python_analysis.py` contains the existing pandas analysis. `visualizations.py` generates the existing Matplotlib chart files in `charts/`. The dashboard adds interactive Plotly charts without removing those outputs.

## Dashboard features

- Eight sidebar pages: Overview, Sales Analytics, Profitability, Customer Analytics, Product Analytics, Geographic Analysis, Payment & Orders, and Business Insights.
- Dark and light themes, global category/city/gender/payment/status/discount filters, hover details and responsive chart layout.
- KPI cards, sortable/searchable customer and performance tables, calculated insights, data quality summary, and filtered CSV downloads.
- No date trend chart or map is shown because the necessary date/coordinate columns are absent.

## Key insights and recommendations

The dashboard calculates leaders and profitability measures dynamically for the selected data. The Business Insights page also reports the concentration of sales in leading cities, discount/profit-margin association, return/cancellation share, and recommendations tied to the lowest-margin category and most common order issues. No results are hard-coded. Correlation is described as an association, not as evidence that discounts cause a margin change.

## Technologies

Python, pandas, SQLite, SQL, Streamlit, Plotly, and Matplotlib. Streamlit runs the web app; Plotly provides interactive charts; pandas prepares the filtered summaries; SQLite demonstrates database-backed reporting.

## Project structure

```text
data analytics/
├── data/
│   ├── raw_data.csv
│   ├── raw_data_backup.csv
│   ├── cleaned_data.csv
│   ├── generate_dataset.py
│   ├── clean_data.py
│   └── sql/
│       ├── ecommerce.db
│       ├── setup_database.py
│       └── ecommerce_analysis.sql
├── dashboard/
│   ├── app.py
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── utils/data.py
├── charts/
├── python_analysis.py
├── visualizations.py
├── requirements.txt
└── README.md
```

The empty `components`, `pages`, and `assets` folders are reserved for future UI modules; navigation and page rendering are kept together in `dashboard/app.py` for beginner-friendly reading.

## Run the project

Open a terminal in the project root. Create and activate a virtual environment (recommended), then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If `py` is unavailable, use `python` in its place. To rerun the existing cleaning pipeline and rebuild the SQLite database:

```powershell
py data/clean_data.py
py data/sql/setup_database.py
```

Start the interactive dashboard:

```powershell
py -m streamlit run dashboard/app.py
```

Run the existing analysis and chart scripts from the project root with `py python_analysis.py` and `py visualizations.py`.

## Future improvements

Add transaction timestamps for sales trends, city coordinates for mapping, product-level identifiers for SKU drill-down, and a stable customer master for richer customer lifetime/value analysis. A scheduled refresh and PDF report can be added when the project needs automated delivery.
