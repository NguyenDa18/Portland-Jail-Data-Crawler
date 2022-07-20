import requests
import pandas as pd
from bs4 import BeautifulSoup

MULT_COUNTY_JAIL_BOOKINGS_URL = "http://www.mcso.us/PAID/Home/SearchResults"
CSV_LOCATION = 'data/data.csv'
INMATE_DATA_CSV_LOCATION = 'data/inmates.csv'

# Go to inmate's link and return a list of charge info
def generate_charges_info(inmate_link):
    inmate_response = requests.get(inmate_link)
    soup = BeautifulSoup(inmate_response.text, 'html.parser')
    charge_infos = soup.find(id='charge-info')

    charge_items = []
    charges = charge_infos.select('div > div > ol')
    for charge in charges:
        for el in charge.find_all('li'):
            charge_type = el.find('span').getText()
            charge_bail = el.find(class_='charge-bail-display').text
            charge_status = el.find(class_='charge-status-value').text
            charge_item = {
                'Type': charge_type,
                'Bail': charge_bail,
                'Status': charge_status
            }
            charge_items.append(charge_item)
    return charge_items

def generate_charge_type_totals(charge_items):
    charge_types = [charge['Type'] for charge in charge_items]
    return pd.Series(charge_types).value_counts().to_dict()

response = requests.post(MULT_COUNTY_JAIL_BOOKINGS_URL)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')
table_input = table.prettify()

# parse dates of column at index 1
table_to_df = pd.read_html(table_input, parse_dates=[1])[0]

# sort by date descending
table_to_df = table_to_df.sort_values(by=["Booking Date", "Name"], ascending = [False, True])


links = table.find_all('a')
INMATE_COLUMNS = ['SWIS ID', 'Name', 'Age', 'Gender', 'Race', 'Height', 'Weight', 'Hair', 'Eyes', 'Arresting Agency', 'Booking Date', 'Assigned Facility', 'Projected Release Date']
jailed_data = []
for link in links:
    booking_url = link.get('href')
    inmate_link = "http://www.mcso.us" + booking_url
    
    # go to inmate's page
    inmate_response = requests.get(inmate_link)
    soup = BeautifulSoup(inmate_response.text, 'html.parser')
    table_input = soup.find('table').prettify()
    booking_table = pd.read_html(table_input)[0][1]
    
    inmate_data = dict(zip(INMATE_COLUMNS, booking_table))
    charge_items = generate_charges_info(inmate_link)
    inmate_data['Charge Type Counts'] = generate_charge_type_totals(charge_items)
    inmate_data['Charges'] = charge_items
    jailed_data.append(inmate_data)

inmates_df = pd.DataFrame(jailed_data).sort_values(by=['Booking Date', 'Name'], ascending=[False, True])
inmates_df.to_csv(INMATE_DATA_CSV_LOCATION, index=False)

# write to file
table_to_df.to_csv(CSV_LOCATION, index=False)