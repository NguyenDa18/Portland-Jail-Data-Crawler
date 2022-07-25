import scrapy
import pandas as pd

class InmateSpider(scrapy.Spider):
    name = 'inmates'
    INMATE_COLUMNS = ['SWIS ID', 'Name', 'Age', 'Gender', 'Race', 'Height', 'Weight', 'Hair', 'Eyes', 'Arresting Agency', 'Booking Date', 'Assigned Facility', 'Projected Release Date']

    def start_requests(self):
        urls = ["http://www.mcso.us/PAID/Home/SearchResults"]
        for url in urls:
            yield scrapy.Request(url = url, 
                        method="POST",
                        callback=self.parse_table)

    def parse_table(self, response):
        table_input = response.css('table').get()
        table_to_df = pd.read_html(table_input, parse_dates=[1])[0]
        table_to_df = table_to_df.sort_values(by=['Booking Date', 'Name'], ascending=[ False, True ])
        table_to_df.to_csv('bookings.csv')