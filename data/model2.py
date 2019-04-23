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
    elif country_rep[place] >= 100:
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
with open('data/allCountry100ppData2014.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'Total_annual_generation', 'Solar','Coal','Gas','Hydro','Oil','Wind',"Waste",'Biomass','Cogeneration','Geothermal','Nuclear','Other','Petcoke']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(country_info_final)

%matplotlib inline

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm 
import statsmodels.formula.api as smf
from statsmodels.graphics.gofplots import ProbPlot

#import csv data
data = pd.read_csv('data/data_100pp_all_variables_clean.csv')

#define data as dataframe type 
df = pd.DataFrame(data)
print(df)   

pd.set_option("precision",4)  # only show 4 digits
corr = df.corr(method="pearson")
print(corr)

# assign dependent and independent / explanatory variables
y = '2014pm25'
x = ['Solar_pct','Coal_pct','Gas_pct','Hydro_pct','Wind_pct','Waste_pct','Biomass_pct','Nuclear_pct','car_data_total','2014co2']

# Ordinary least squares regression with constant term
model = sm.OLS(df[y], sm.add_constant(df[x])).fit()
print(model.summary())

#print arrays of important values
print(model.params)
print("\n")
print(model.pvalues)
print("\n")
print('R2: ', model.rsquared)

plt.style.use('seaborn') # pretty matplotlib plots

plt.rc('font', size=14)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)


# fitted values (need a constant term for intercept)
model_fitted_y = model.fittedvalues

# model residuals
model_residuals = model.resid

# normalized residuals
model_norm_residuals = model.get_influence().resid_studentized_internal

# absolute residuals
model_abs_resid = np.abs(model_residuals)

# leverage, from statsmodels internals
model_leverage = model.get_influence().hat_matrix_diag

# cook's distance, from statsmodels internals
model_cooks = model.get_influence().cooks_distance[0]

#Residual Plot
plot_lm_1 = plt.figure(1)
plot_lm_1.set_figheight(8)
plot_lm_1.set_figwidth(12)

plot_lm_1.axes[0] = sns.residplot(model_fitted_y, '2014pm25', data=data, 
                          lowess=True, 
                          scatter_kws={'alpha': 0.5}, 
                          line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_1.axes[0].set_title('Residuals vs Fitted')
plot_lm_1.axes[0].set_xlabel('Fitted values')
plot_lm_1.axes[0].set_ylabel('Residuals')

# annotations
abs_resid = model_abs_resid.sort_values(ascending=False)
abs_resid_top_3 = abs_resid[:3]

for i in abs_resid_top_3.index:
    plot_lm_1.axes[0].annotate(i, 
                               xy=(model_fitted_y[i], 
                                   model_residuals[i]));
    
#QQ plot
QQ = ProbPlot(model_norm_residuals)
plot_lm_2 = QQ.qqplot(line='45', alpha=0.5, color='#4C72B0', lw=1)

plot_lm_2.set_figheight(8)
plot_lm_2.set_figwidth(12)

plot_lm_2.axes[0].set_title('Normal Q-Q')
plot_lm_2.axes[0].set_xlabel('Theoretical Quantiles')
plot_lm_2.axes[0].set_ylabel('Standardized Residuals');

# annotations
abs_norm_resid = np.flip(np.argsort(np.abs(model_norm_residuals)), 0)
abs_norm_resid_top_3 = abs_norm_resid[:3]

for r, i in enumerate(abs_norm_resid_top_3):
    plot_lm_2.axes[0].annotate(i, 
                               xy=(np.flip(QQ.theoretical_quantiles, 0)[r],
                                   model_norm_residuals[i]));
    
# Cooks Distance
plot_lm_4 = plt.figure(4)
plot_lm_4.set_figheight(8)
plot_lm_4.set_figwidth(12)

plt.scatter(model_leverage, model_norm_residuals, alpha=0.5)
sns.regplot(model_leverage, model_norm_residuals, 
            scatter=False, 
            ci=False, 
            lowess=True,
            line_kws={'color': 'red', 'lw': 1, 'alpha': 0.8})

plot_lm_4.axes[0].set_xlim(0, 0.20)
plot_lm_4.axes[0].set_ylim(-3, 5)
plot_lm_4.axes[0].set_title('Residuals vs Leverage')
plot_lm_4.axes[0].set_xlabel('Leverage')
plot_lm_4.axes[0].set_ylabel('Standardized Residuals')

# annotations
leverage_top_3 = np.flip(np.argsort(model_cooks), 0)[:3]

for i in leverage_top_3:
    plot_lm_4.axes[0].annotate(i, 
                               xy=(model_leverage[i], 
                                   model_norm_residuals[i]))
    
# shenanigans for cook's distance contours
def graph(formula, x_range, label=None):
    x = x_range
    y = formula(x)
    plt.plot(x, y, label=label, lw=1, ls='--', color='red')

p = len(model.params) # number of model parameters

graph(lambda x: np.sqrt((0.5 * p * (1 - x)) / x), 
      np.linspace(0.001, 0.200, 50), 
      'Cook\'s distance') # 0.5 line
graph(lambda x: np.sqrt((1 * p * (1 - x)) / x), 
      np.linspace(0.001, 0.200, 50)) # 1 line
plt.legend(loc='upper right');