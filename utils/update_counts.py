import json
import pandas as pd
import datetime

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

def generate_stats_for_category(column):
    stat_counts = INMATES_DETAILS_DF[column.capitalize()].value_counts()
    stat_counts = stat_counts.to_dict()
    stat_counts = {**stat_counts, 'Date': CURRENT_DATE}
    update_stats_file(stat_counts, f'../counts/inmate_counts_{column}.json')


generate_stats_for_category('gender')
generate_stats_for_category('race')
# generate_stats_for_category('eyes')
