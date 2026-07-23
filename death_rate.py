import pandas as pd
import matplotlib.pyplot as plt


# Dropping first 2 rows - metadata
def death_rate_processing(death_rate_path):
    
    death_rate_df= pd.read_excel(death_rate_path, engine='xlrd')
    temp_list1 = death_rate_df.iloc[2].tolist()[:4]
    temp_list2 = death_rate_df.iloc[2].tolist()[4:]
    temp_list2 = list(map(int, temp_list2))
    temp_list1.extend(temp_list2) #creating column headers

    death_rate_df.columns = temp_list1 #resetting default columns
    death_rate_df = death_rate_df.iloc[3:].reset_index(drop=True)


    # Checking columns with all null values and dropping them.
    for i in death_rate_df.columns:
        if death_rate_df[i].isna().all():
            death_rate_df.drop(columns=i, inplace=True)


    # Column of year 2025 dropped
    # Combining income data with main df

    df_income = pd.read_excel(death_rate_path, sheet_name='Metadata - Countries', engine='xlrd')
    df_income.drop(columns=['Country Code','SpecialNotes','TableName'], inplace=True)
    # df_income

    # Filling missing values with custom text for better interpretation in 'IncomeGroup' and 'Region' columns.

    death_rate_df = pd.concat([death_rate_df, df_income], axis=1)
    death_rate_df['IncomeGroup'] = death_rate_df['IncomeGroup'].fillna('Income Unavailable')
    death_rate_df['Region'] = death_rate_df['Region'].fillna('Region Unavailable')
    return death_rate_df



