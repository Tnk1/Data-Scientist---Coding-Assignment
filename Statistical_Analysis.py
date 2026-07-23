import pandas as pd
import input_paths
import copy
from life_expectancy_at_birth import life_expectancy_birth
from birth_male_female import life_expectancy_male
from birth_male_female import life_expectancy_female
from fertility_rate import fertility_rate_processing
# Statistical Analysis
print('****************************Statistical Analysis****************************\n\n')

df_total_birth = life_expectancy_birth(input_paths.total_birth_path)
df_birth_male = life_expectancy_male(input_paths.life_expectancy_male_path)
df_birth_female = life_expectancy_female(input_paths.life_expectancy_female_path)
df_fertility = fertility_rate_processing(input_paths.fertility_path)


# 1a : For which income group has the difference in average life expectancy of 
# men and women changed the most between 1960 and 2023?

print('1a : For which income group has the difference in average life expectancy of men and women changed the most between 1960 and 2023?\n') 
difference = copy.deepcopy(df_birth_male.iloc[:,0:4])
difference = pd.concat([difference,copy.deepcopy(df_birth_male.iloc[:,-2:])], axis=1)
difference
#difference of life expectancies over the years for male and female
for i in range(1960, 2025, 1):
    difference[i] = abs(df_birth_male[i] - df_birth_female[i])
#Grouped values based on IncomeGroup for each year
difference['Change'] = abs(difference[1960] - difference[2023])
result1 = (difference.groupby('IncomeGroup')['Change'].max())
print(f"Income Group with significant difference: {result1.idxmax()}")

print('\n\n')

# 1b : For which income group has variability in life expectancy at birth changed 
# the most between 1960 and 2023? 

print('1b : For which income group has variability in life expectancy at birth changed the most \n between 1960 and 2023? \n')
variance_1960 = df_total_birth.groupby('IncomeGroup')[1960].var()
variance_1960 
variance_2023 = df_total_birth.groupby('IncomeGroup')[2023].var()
variance_2023 
result2 = abs(variance_1960 - variance_2023)
print(f'Income Group with highest variability : {result2.idxmax()}')
result2

print('\n\n')

# 1c : Which countries have the highest correlation between fertility rate and life 
# expectancy at birth over the years (either positive or negative)? Which 
# countries have the lowest correlation?  

print('1c : Which countries have the highest correlation between fertility rate and life expectancy at birth over the years (either positive or negative)? Which countries have the lowest correlation?\n')

#mapping Country name with correlation data of life expectancy at birth and fertility data
dictionary = {}
for i, j in zip(df_total_birth.loc[:,'Country Name'], range(len(df_total_birth))):
    dictionary[i] = df_total_birth.loc[j,1960:2023].corr(df_fertility.loc[j,1960:2023], method = 'pearson')

#dataframe creation for correlation data
correlation_df1 = pd.DataFrame(list(dictionary.items()), columns=['Country', 'Correlation'])
correlation_df1
max1 = correlation_df1['Correlation'].max()
print('Country with most positive correlation with life expectancy at birth and fertility rate : \n')
print(correlation_df1.loc[correlation_df1['Correlation'] == max1])
print('\n')

max2 = correlation_df1['Correlation'].min()
print('Country with most negative correlation with life expectancy at birth and fertility rate : \n')
print(correlation_df1.loc[correlation_df1['Correlation'] == max2])
print('\n')

min = correlation_df1['Correlation'].abs().min()
print('Country with least correlation with life expectancy at birth and fertility rate : \n')
print(correlation_df1.loc[correlation_df1['Correlation'] == min])

