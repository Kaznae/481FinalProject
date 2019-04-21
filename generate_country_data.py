import pandas
import math
import csv

plants = pandas.read_csv("data/projdata_pp.csv")

valid_countries = []
#generate countries with at least x power plant entries:
country_rep = {}
for place in plants['country_long']:
    if place not in country_rep:
        country_rep[place] = 1
    elif country_rep[place] >= 1 and place not in valid_countries:
        valid_countries.append(place)
        continue
    else:
        country_rep[place] += 1


country_info = {}

for index, row in plants.iterrows():
    #skip low data countries, and commission years past 2014
    if row['country_long']not in valid_countries or (not math.isnan(row['commissioning_year']) and int(row['commissioning_year']) > 2014):
        continue
    if row['country_long'] not in country_info:
        country_info[row['country_long']] = {'Total_annual_generation':row['estimated_anual_generation_gwh'],'Solar':0,'Coal':0,'Gas':0,'Hydro':0,'Oil':0,'Wind':0,"Waste":0,'Biomass':0,'Cogeneration':0,'Geothermal':0,'Nuclear':0,'Petcoke':0,'Other':0}
        country_info[row['country_long']][row['fuel1']] += 1
    else:
        country_info[row['country_long']]['Total_annual_generation'] += row['estimated_anual_generation_gwh']
        country_info[row['country_long']][row['fuel1']] += 1

country_info_final = []
for info in country_info:
    temp = {'Name':info}
    temp.update(country_info[info])
    country_info_final.append(temp)

#for info in country_info_final:
with open('allCountryData2014.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'Total_annual_generation', 'Solar','Coal','Gas','Hydro','Oil','Wind',"Waste",'Biomass','Cogeneration','Geothermal','Nuclear','Other','Petcoke']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(country_info_final)

