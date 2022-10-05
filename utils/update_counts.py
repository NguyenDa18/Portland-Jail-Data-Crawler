import json
import pandas as pd
import datetime

CHARGES_COLUMNS = ["Charge_type", "Bail", "Charge_status", "Name"]
INMATES_CHARGES_DF = pd.read_csv("../csvs/inmate_charges.csv", names=CHARGES_COLUMNS, header=None)
INMATES_DETAILS_DF = pd.read_csv("../csvs/inmate_details.csv")

# store current date as YYYY-MM-DD
CURRENT_DATE = datetime.date.today().strftime("%Y-%m-%d")

def update_stats_file(new_data, filename):
    with open(filename, 'r+') as file:
        current_data = json.load(file)
        current_data["counts"].append(new_data)
        # set file's current position at offset
        file.seek(0)
        json.dump(current_data, file, indent=3)
        file.close()

def generate_stats_for_category(df, column):
    stat_counts = df[column.capitalize()].value_counts()[:20]
    stat_counts = stat_counts.to_dict()
    stat_counts = {**stat_counts, 'Date': CURRENT_DATE}
    update_stats_file(stat_counts, f'../counts/inmate_counts_{column}.json')


generate_stats_for_category(INMATES_DETAILS_DF, 'gender')
generate_stats_for_category(INMATES_DETAILS_DF, 'race')
generate_stats_for_category(INMATES_CHARGES_DF, 'charge_type')
generate_stats_for_category(INMATES_CHARGES_DF, 'charge_status')
