import pandas
import math
import csv

'''
generate countries with at least 100 power plant entries:

country_rep = {}
for place in plants['country_long']:
    if place in valid_countries:
        continue
    elif place not in country_rep:
        country_rep[place] = 1
    elif country_rep[place] >= 100:
        valid_countries.append(country_rep[place])
        continue
    else:
        country_rep[place] += 1
'''

plants = pandas.read_csv("data/projdata_pp.csv")

valid_countries = ['Argentina', 'Australia', 'Austria', 'Brazil', 'Canada', 'Chile', 'China', 'Finland',
'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Italy', 'Japan', 'Mexico','Norway',
'Portugal', 'Russia', 'South Korea', 'Spain,Sweden', 'Switzerland', 'Thailand',
'United Kingdom', 'United States of America', 'Vietnam']

country_info = {}

for index, row in plants.iterrows():
    #skip low data countries, plants with no comission year, and commission years past 2010
    #change third condition to set different cutoff years
    if row['country_long'] not in valid_countries or math.isnan(row['commissioning_year']) or int(row['commissioning_year']) > 2010:
        continue
    if row['country_long'] not in country_info:
        country_info[row['country_long']] = {'total_annual_generation':row['estimated_anual_generation_gwh'],row['fuel1']:1}
    else:
        country_info[row['country_long']]['total_annual_generation'] += row['estimated_anual_generation_gwh']
        if row['fuel1'] not in country_info[row['country_long']]:
            country_info[row['country_long']][row['fuel1']] = 1
        else:
            country_info[row['country_long']][row['fuel1']] += 1

with open('data/country_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in country_info.items():
       writer.writerow([key, value])
