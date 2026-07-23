#Data Visualizations
import pandas as pd
import input_paths
import matplotlib.pyplot as plt
import copy
from life_expectancy_at_birth import life_expectancy_birth
from birth_male_female import life_expectancy_male
from birth_male_female import life_expectancy_female
from fertility_rate import fertility_rate_processing
# Statistical Analysis

df_total_birth = life_expectancy_birth(input_paths.total_birth_path)
df_birth_male = life_expectancy_male(input_paths.life_expectancy_male_path)
df_birth_female = life_expectancy_female(input_paths.life_expectancy_female_path)
fertility_df = fertility_rate_processing(input_paths.fertility_path)


# 2a. Create a time-series line chart showing how life expectancy at birth has 
# changed over the years for each income group.
# creating dataframe for Income comparison
merged_temp = df_total_birth.loc[:,1960:2023]
merged_temp = pd.concat([df_total_birth['IncomeGroup'], merged_temp], axis = 1)
merged_temp
#grouped data based on average values in every Income group is obtained. The dataframe is transposed for better comparison.
transposed_df = merged_temp.groupby('IncomeGroup')[merged_temp.columns[1:]].mean().T
transposed_df
transposed_df.index
transposed_df.plot(figsize=(12,6))

plt.title("Life Expectancy at Birth by Income Group")
plt.xlabel("Year")
plt.ylabel("Average Life Expectancy")
plt.legend(title="Income Group")
plt.grid(True,linestyle='--', alpha=1)
plt.show()

# 2b. Create a world map where each country is color coded according to how 
# high or low the life expectancy at birth is in 2023. 
# !pip install nbformat

#Opens up in browser
import plotly.express as px

fig = px.choropleth(
    df_total_birth,
    locations='Country Code',      # ISO-3 codes
    color=2023,                    # Life expectancy values
    hover_name='Country Name',
    color_continuous_scale='Viridis',
    title='Life Expectancy at Birth (2023)'
)

fig.show(renderer='browser')


# 2c. For the year 1960, rank the countries by life expectancy at birth and classify them into 
# five buckets of roughly equal size. The buckets should be called 'Very high life expectancy', 'High life expectancy', 'Medium life expectancy', 'Low life expectancy', 'Very low life expectancy'. Repeat this for the 2023 data. Create a Sankey diagram showing from which category in 1960 countries have moved to in 2023.

bucket_df = pd.DataFrame(columns=['Data_1960','Data_2023'])
bucket_df['Data_1960'] = pd.qcut(df_total_birth[1960], q=5, labels=['Very low life expectancy','Low life expectancy','Medium life expectancy','High life expectancy','Very high life expectancy']) #Quinitle split for roughly 5 equal segments
bucket_df['Data_2023'] = pd.qcut(df_total_birth[2023], q=5, labels=['Very low life expectancy','Low life expectancy','Medium life expectancy','High life expectancy','Very high life expectancy'])

#obtaining count of each combination from 1960 and 2023.
bucket_df = bucket_df.groupby(['Data_1960', 'Data_2023']).size().reset_index(name='Count')

#Creating nodes and links for customised comparison of data flow. 
#Opens up in browser
import plotly.graph_objects as go

NODES = dict(
    label=[
        'Very low (1960)',
        'Low (1960)',
        'Medium (1960)',
        'High (1960)',
        'Very high (1960)',

        'Very low (2023)',
        'Low (2023)',
        'Medium (2023)',
        'High (2023)',
        'Very high (2023)'
    ]
)

LINKS = dict(
    source=[0, 0 , 0, 0, 0, 1 ,1 ,1 ,1 ,1 ,2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4],
    target=[5, 6, 7, 8, 9, 5, 6, 7, 8, 9,5, 6, 7, 8, 9,5, 6, 7, 8, 9,5, 6, 7, 8, 9,],
    value = list(bucket_df.loc[:,'Count'])
)

fig = go.Figure(
    go.Sankey(
        node=NODES,
        link=LINKS
    )
)

fig.show(renderer="browser")
