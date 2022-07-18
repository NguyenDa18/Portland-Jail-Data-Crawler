import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

MULT_COUNTY_JAIL_BOOKINGS_URL = "http://www.mcso.us/PAID/Home/SearchResults"

response = requests.post(MULT_COUNTY_JAIL_BOOKINGS_URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
table_input = table.prettify()

# parse dates of column at index 1
table_to_df = pd.read_html(table_input, parse_dates=[1])[0]