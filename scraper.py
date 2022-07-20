import requests
import pandas as pd
from bs4 import BeautifulSoup

MULT_COUNTY_JAIL_BOOKINGS_URL = "http://www.mcso.us/PAID/Home/SearchResults"
CSV_LOCATION = 'data/data.csv'

response = requests.post(MULT_COUNTY_JAIL_BOOKINGS_URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
table_input = table.prettify()

# parse dates of column at index 1
table_to_df = pd.read_html(table_input, parse_dates=[1])[0]

# sort by date descending
table_to_df = table_to_df.sort_values(by=["Booking Date", "Name"], ascending = [False, True])

# write to file
table_to_df.to_csv(CSV_LOCATION, index=False)