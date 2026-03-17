# 🏠 Ahmedabad Real Estate — Web Scraping & EDA

A end-to-end data project that scrapes live real estate listings from [realestateindia.com](https://www.realestateindia.com), cleans and structures the raw data, and performs exploratory data analysis to uncover pricing trends across Ahmedabad's property market.

> **Learning focus:** This project was built to get hands-on experience with Selenium for browser automation, BeautifulSoup for HTML parsing, pandas for data wrangling, and seaborn/matplotlib for visualization.

---

## 📌 Project Highlights

- **Browser Automation with Selenium** — Automated Firefox via Selenium + GeckoDriver to dynamically scroll and click "Load More" on paginated real estate listings, capturing data that doesn't exist in static HTML.
- **HTML Parsing with BeautifulSoup** — Extracted structured fields (project name, builder, location, price, RERA status, property type, possession status, total units) from raw saved page source using targeted CSS class selectors.
- **Data Cleaning & Feature Engineering** — Standardized messy price strings (e.g. `"45 Lac - 1.2 Cr"`) into consistent numeric min/max/average values in Lakhs; normalized builder names, property type categories, and handled missing values.
- **Exploratory Data Analysis** — Investigated pricing patterns across locations, builders, property types, and RERA registration status using bar plots, count plots, and box plots.
- **Actionable Insights** — Identified the top 10 highest-priced locations and builders in Ahmedabad, visualized the dominance of apartments in the market, and compared price distributions between RERA-registered and non-registered projects.

---

## 🗂️ Project Structure

```
├── WorkingScraper.py        # Selenium scraper — scrolls, clicks Load More, saves page source
├── Extract-DF-Ahm.py        # BeautifulSoup parser — extracts fields and outputs CSV
├── EDA-Ahm-Final.ipynb      # Jupyter notebook — data cleaning, feature engineering, EDA plots
├── Ahemdabad_source.txt     # Raw saved HTML page source (scraper output)
└── Pyfile_ahm_data.csv      # Cleaned structured dataset (parser output)
```

---

## ⚙️ Setup & Usage

### Prerequisites

- Python 3.8+
- Firefox browser
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (v0.36.0 recommended)

### Install dependencies

```bash
pip install selenium beautifulsoup4 pandas numpy matplotlib seaborn
```

### Step 1 — Scrape the listings

Update the `path_to_file` and `executable_path` variables in `WorkingScraper.py` to match your local paths, then run:

```bash
python WorkingScraper.py
```

This will open Firefox, scroll through the listings page, and save the raw HTML to `source.txt`. Adjust `scroll_no` in the `while` loop to control how many "Load More" clicks to perform.

### Step 2 — Extract & build the dataset

```bash
python Extract-DF-Ahm.py
```

This reads `Ahemdabad_source.txt`, parses all listing fields, converts prices to Lakhs, and saves the cleaned data to `Pyfile_ahm_data.csv`.

### Step 3 — Run the EDA

Open `EDA-Ahm-Final.ipynb` in Jupyter and run all cells to explore the visualizations.

---

## 📊 EDA Visualizations

| Chart | Description |
|---|---|
| RERA Registration vs Possession Status | Count plot comparing RERA-registered vs non-registered projects across possession stages |
| Distribution of Property Types | Frequency of Apartments, Plots, Villas, Commercial spaces, etc. |
| Top 10 Locations by Avg Price | Bar chart of the most expensive areas in Ahmedabad |
| Top 10 Builders by Avg Price | Bar chart ranking builders by their average listing price |
| Price Distribution by Property Type | Box plot showing price spread across property categories |
| Price Distribution by RERA Status | Box plot comparing pricing of RERA vs non-RERA projects |

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| `Selenium` | Browser automation & dynamic page scraping |
| `BeautifulSoup4` | HTML parsing & data extraction |
| `pandas` | Data cleaning, transformation, and analysis |
| `numpy` | Numerical operations & NaN handling |
| `matplotlib` / `seaborn` | Data visualization |

---

## 📝 Notes

- The scraper saves raw HTML locally so parsing can be done offline without re-scraping.
- Prices are normalized to **Indian Lakhs (₹)** for consistent comparison (1 Crore = 100 Lakhs).
- Builder names are cleaned by stripping the "By" prefix present in raw listings.
- Property types are simplified into broad categories (Apartment, Plot, House/Villa, Office Space, Commercial Shop) for cleaner analysis.
