import pandas as pd
import matplotlib.pyplot as plt


def life_expectancy_birth(df_total_birth_path):

    df_total_birth = pd.read_excel(df_total_birth_path, engine='xlrd')
    temp_list1 = df_total_birth.iloc[2].tolist()[:4] #strings
    temp_list2 = df_total_birth.iloc[2].tolist()[4:] #integers
    temp_list2 = list(map(int, temp_list2))
    temp_list1.extend(temp_list2) #creating column headers

    df_total_birth.columns = temp_list1 #resetting default columns
    df_total_birth = df_total_birth.iloc[3:].reset_index(drop=True)

    # Checking columns with all null values and dropping them.
    for i in df_total_birth.columns:
        if df_total_birth[i].isna().all():
            df_total_birth.drop(columns=i, inplace=True)

    # Column of year 2025 dropped
    # Combining income data with main df
    df_income = pd.read_excel(df_total_birth_path, sheet_name='Metadata - Countries', engine='xlrd')
    df_income.drop(columns=['Country Code','SpecialNotes','TableName'], inplace=True)
    df_income
    # Filling missing values with custom text for better interpretation in 'IncomeGroup' and 'Region' columns.
    df_total_birth = pd.concat([df_total_birth, df_income], axis=1)
    df_total_birth['IncomeGroup'] = df_total_birth['IncomeGroup'].fillna('Income Unavailable')
    df_total_birth['Region'] = df_total_birth['Region'].fillna('Region Unavailable')
    return df_total_birth






