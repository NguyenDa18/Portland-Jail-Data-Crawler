# Multnomah County Jail Crawler

[![scraper-pdx-jail](https://github.com/NguyenDa18/PDX-Jail-Data-Crawler/actions/workflows/main.yml/badge.svg)](https://github.com/NguyenDa18/PDX-Jail-Data-Crawler/actions/workflows/main.yml)

![Portland Justice](https://media.giphy.com/media/SJXKIfZVq5EWieBZbX/giphy.gif)

## Purpose

Crawl through bookings of PDX Jail Database for data analysis and data transparency purposes. Update data files with scheduled jobs courtesy of GitHub actions.

- Visit Multnomah County Online Inmate Data website: use URL for all inmates in custody
- Scrape inmate names and booking dates and update `csvs/inmate_bookings.csv` file
- Visit each inmate link and update `csvs/inmate_details.csv` with inmate details and charges against them

## Using
- BeautifulSoup
- Pandas
- GitHub Actions (for cron job running scraper)

## Enhancements
- [X] Storing data to a Database
- [X] Optimizing crawling
- [X] Using Scrapy Spider instead of BeautifulSoup
- [ ] Creating UI for viewing data
- [ ] Send notification when a "red flag" is released

## Running It Yourself 

**Prerequisite**: Python 3 needs to be installed

1. Clone repo
2. Activate Virtual Environment

```
source venv/bin/activate
```

3. Install dependencies in Virtual Environment

```
pip install -r requirements.txt
```

4. Best way to experiment is using Jupyter Notebook:

```
jupyter notebook
```

Then run experimental code in `Sandbox Notebook.ipynb`

