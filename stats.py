import pandas as pd
import statsmodels.api as sm 

data = pd.read_csv('data/data_all_variables_clean.csv')

df = pd.DataFrame(data)
#print(df)   

pd.set_option("precision",4)  # only show 4 digits

#correlation table
corr = df.corr(method="pearson")

corr

# assign dependent and independent / explanatory variables
    
y = '2014pm25'
x = ['Coal_pct','Gas_pct','Oil_pct','Waste_pct','Biomass_pct','2014co2']

# Ordinary least squares regression
model_Simple = sm.OLS(df[y], df[x]).fit()

# Add a constant term:
model = sm.OLS(df[y], sm.add_constant(df[x])).fit()

model.summary()