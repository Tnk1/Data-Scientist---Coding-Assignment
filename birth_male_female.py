import pandas as pd
import matplotlib.pyplot as plt
import copy


# Male Life Expectancy

def life_expectancy_male(life_expectancy_male_path):
    df_birth_male = pd.read_excel(life_expectancy_male_path, engine='xlrd')

    temp_list1 = df_birth_male.iloc[2].tolist()[:4] #strings
    temp_list2 = df_birth_male.iloc[2].tolist()[4:] #integers
    temp_list2 = list(map(int, temp_list2))
    temp_list1.extend(temp_list2) #creating column headers

    df_birth_male.columns = temp_list1 #resetting default columns
    df_birth_male = df_birth_male.iloc[3:].reset_index(drop=True)

    # Checking columns with all null values and dropping them.
    for i in df_birth_male.columns:
        if df_birth_male[i].isna().all():
            df_birth_male.drop(columns=i, inplace=True) #column of year 2025 dropped

    
    # Combining income data with main df
    df_income = pd.read_excel(life_expectancy_male_path, sheet_name='Metadata - Countries',engine='xlrd')
    df_income.drop(columns=['SpecialNotes','TableName'], inplace=True) #dropping low priority columns
    df_income
    # Filling missing values with custom text for better interpretation in 'IncomeGroup' and 'Region' columns.
    df_birth_male = pd.merge(df_birth_male, df_income, on='Country Code')
    df_birth_male['IncomeGroup'] = df_birth_male['IncomeGroup'].fillna('Income Unavailable')
    df_birth_male['Region'] = df_birth_male['Region'].fillna('Region Unavailable')
    df_birth_male.to_csv('df_birth_male.csv', index=False) #saving file for dashboard usage.
    return df_birth_male

# Female Life Expectancy
def life_expectancy_female(life_expectancy_female_path):
    df_birth_female = pd.read_excel(life_expectancy_female_path, engine='xlrd')

    temp_list1 = df_birth_female.iloc[2].tolist()[:4] #strings
    temp_list2 = df_birth_female.iloc[2].tolist()[4:] #integers
    temp_list2 = list(map(int, temp_list2))
    temp_list1.extend(temp_list2) #creating column headers

    df_birth_female.columns = temp_list1 #resetting default columns
    df_birth_female = df_birth_female.iloc[3:].reset_index(drop=True)

    # Checking columns with all null values and dropping them.
    for i in df_birth_female.columns:
        if df_birth_female[i].isna().all():
            df_birth_female.drop(columns=i, inplace=True)

    #column of year 2025 dropped
    df_income = pd.read_excel(life_expectancy_female_path, sheet_name='Metadata - Countries',engine='xlrd')
    df_income.drop(columns=['SpecialNotes','TableName'], inplace=True)
    df_income
    # Filling missing values with custom text for better interpretation in 'IncomeGroup' and 'Region' columns.
    df_birth_female = pd.merge(df_birth_female, df_income, on='Country Code')
    df_birth_female['IncomeGroup'] = df_birth_female['IncomeGroup'].fillna('Income Unavailable')
    df_birth_female['Region'] = df_birth_female['Region'].fillna('Region Unavailable')
    df_birth_female.to_csv('df_birth_female.csv', index=False) #saving file for dashboard usage.
    return df_birth_female




# -----------------------------------End of Script-----------------------------------------
