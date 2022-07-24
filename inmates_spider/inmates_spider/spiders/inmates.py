import scrapy
import pandas as pd

class InmateSpider(scrapy.Spider):
    name = 'inmates'

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
        table_to_df.to_csv('../../../data/demo.csv')

        inmate_links = response.xpath('//*[@class="search-results"]//a/@href').getall()
        for link in inmate_links:
            url = response.urljoin(link)
            yield response.follow(url = url, callback = self.parse_inmate_data)

    def parse_inmate_data(self, response):
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
        yield {
            'Charges': charge_items
        }