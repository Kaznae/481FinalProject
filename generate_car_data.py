import pandas
import math
import csv

cars = pandas.read_csv('data/Total_in-use-All-Vehicles.csv')
countries = open('country_list.txt').read().split('\n')

for i in range(len(countries)):
    countries[i] = countries[i].upper()

car_info = []

for index, row in cars.iterrows():
    #skip countries we dont have plant info for
    if row['Countries'] not in countries:
        print(row['Countries'])
        continue
    #up to 2013
    total = row['2005'] + row['2006'] + row['2007'] + row['2008'] + row['2009'] + row['2010'] + row['2011'] + row['2012'] + row['2013']
    car_info.append({'Name':row['Countries'],'2005':row['2005'],'2006':row['2006'],'2007':row['2007'],'2008':row['2008'],'2009':row['2009'],'2010':row['2010'],'2011':row['2011'],'2012':row['2012'],'2013':row['2013'],'total':total})

keys = car_info[0].keys()
with open('data/car_data.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(car_info)
