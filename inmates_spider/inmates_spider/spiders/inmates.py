import scrapy
import pandas as pd
import os
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']

class InmateSpider(scrapy.Spider):
    name = 'inmates'
    INMATE_COLUMNS = ['SWIS ID', 'Name', 'Age', 'Gender', 'Race', 'Height', 'Weight', 'Hair', 'Eyes', 'Arresting Agency', 'Booking Date', 'Assigned Facility', 'Projected Release Date']

    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client.data

    def start_requests(self):
        # empty collection before inserting new inmates
        self.db.inmates_charges.drop()
        urls = ["http://www.mcso.us/PAID/Home/SearchResults"]
        for url in urls:
            yield scrapy.Request(url = url, 
                        method="POST",
                        callback=self.parse_table)

    def parse_table(self, response):
        inmate_table_rows = []
        rows = response.css('table tbody tr')

        for row in rows:
            name_column = row.css('tr td')[0]
            booking_column = row.css('tr td')[1]
            inmate_name = name_column.css('a::text').get()
            inmate_url = name_column.css('a::attr(href)').get()
            booking_date = booking_column.css('::text').get()
            inmate_row = {
                'Name': inmate_name,
                'Booking Date': booking_date,
                'URL': inmate_url
            }
            inmate_table_rows.append(inmate_row)
        inmate_df = pd.DataFrame(inmate_table_rows)

         # https://www.programiz.com/python-programming/datetime/strftime
        inmate_df['Booking Date'] = pd.to_datetime(inmate_df['Booking Date'], format='%d %B %Y')
        inmate_df = inmate_df.sort_values(by=['Booking Date', 'Name'], ascending=[ False, True ])
        inmate_links = inmate_df['URL']
        for link in inmate_links:
            url = response.urljoin(link)
            yield response.follow(url = url, callback = self.parse_inmate_data)
        inmate_df.drop('URL', axis=1, inplace=True)
        inmate_df.to_csv('../../../csvs/inmate_bookings.csv', index=False)

    def parse_inmate_data(self, response):
        inmates_table = response.css('table').get()
        booking_table = pd.read_html(inmates_table)[0][1]
        inmate_data = dict(zip(self.INMATE_COLUMNS, booking_table))

        charge_types = response.css('span.charge-description-display::text').getall()
        charge_bail_amounts = response.css('span.charge-bail-value::text').getall()
        charge_statuses = response.css('span.charge-status-value::text').getall()
        charge_items = []
        for c_type, c_bail, c_status in zip(charge_types, charge_bail_amounts, charge_statuses):
            charge_item = {
                'Type': c_type,
                'Bail': c_bail,
                'Status': c_status
            }
            charge_items.append(charge_item)
        charge_types = [charge['Type'] for charge in charge_items]
        charge_type_totals = pd.Series(charge_types).value_counts().to_dict()
        charge_type_totals['SWID'] = inmate_data['SWIS ID']
        charge_type_totals['Name'] = inmate_data['Name']
        
        # make copy for db so ObjectID isn't part of CSV
        charge_totals_dbitem = {
            "Name": inmate_data['Name'],
            "SWIS ID": inmate_data['SWIS ID'],
            "charges": {
                "counts": dict(charge_type_totals)
            }
        }

        inmate_data['Charge Type Counts'] = charge_type_totals
        inmate_data['Charges'] = charge_items

        self.db.inmates_charges.insert_one(charge_totals_dbitem)

        yield inmate_data