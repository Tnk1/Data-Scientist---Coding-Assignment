import pandas as pd
import matplotlib.pyplot as plt


def fertility_rate_processing(df_fertility_path):

    df_fertility = pd.read_excel(df_fertility_path, engine='xlrd')
    temp_list1 = df_fertility.iloc[2].tolist()[:4] #integers
    temp_list2 = df_fertility.iloc[2].tolist()[4:] #strings
    temp_list2 = list(map(int, temp_list2))
    temp_list1.extend(temp_list2) #creating column headers

    df_fertility.columns = temp_list1 #resetting default columns
    df_fertility = df_fertility.iloc[3:].reset_index(drop=True)

    # Checking columns with all null values and dropping them.
    for i in df_fertility.columns:
        if df_fertility[i].isna().all():
            df_fertility.drop(columns=i, inplace=True)


    # Combining income data with main df
    df_income = pd.read_excel(df_fertility_path, sheet_name='Metadata - Countries', engine='xlrd')

    len(df_income['Country Code'].unique())  #checking if there are redundant values in the columns
    df_income.drop(columns=['Country Code','SpecialNotes','TableName'], inplace=True)

    # Filling missing values with custom text for better interpretation in 'IncomeGroup' and 'Region' columns.
    df_fertility = pd.concat([df_fertility, df_income], axis=1)
    df_fertility['IncomeGroup'] = df_fertility['IncomeGroup'].fillna('Income Unavailable')
    df_fertility['Region'] = df_fertility['Region'].fillna('Region Unavailable')
    return df_fertility





