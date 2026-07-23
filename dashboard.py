import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_ag_grid as dag
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import input_paths
from life_expectancy_at_birth import life_expectancy_birth
from birth_male_female import life_expectancy_male
from birth_male_female import life_expectancy_female
from fertility_rate import fertility_rate_processing
# Statistical Analysis

df_total_birth = life_expectancy_birth(input_paths.total_birth_path)
df_birth_male = life_expectancy_male(input_paths.life_expectancy_male_path)
df_birth_female = life_expectancy_female(input_paths.life_expectancy_female_path)
df_fertility = fertility_rate_processing(input_paths.fertility_path)
df_death_rate = fertility_rate_processing(input_paths.death_rate_path)


#Dashboard Creation 


DATASETS = {
    "Life Expectancy : Male": df_birth_male,
    "Life Expectancy : Female": df_birth_female,
    "Birth Rate": df_total_birth,
    "Death Rate": df_death_rate,
    "Fertility Rate": df_fertility
}


MALE_DF = df_birth_male
FEMALE_DF = df_birth_female


for df in DATASETS.values():
    df.columns = df.columns.astype(str)

MALE_DF.columns = MALE_DF.columns.astype(str)
FEMALE_DF.columns = FEMALE_DF.columns.astype(str)

# ==========================================================
# APP
# ==========================================================

app = Dash(__name__)

# ==========================================================
# LAYOUT
# ==========================================================

app.layout = html.Div(
    [
        html.H1(
            "NXP - Team HDA : Analysis and Deeper Insights, as always! ",
            style={
                "textAlign": "center",
                "color": "#236AE6"
            }
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Dataset"),
                        dcc.Dropdown(
                            id="dataset-dropdown",
                            options=[
                                {
                                    "label": dataset,
                                    "value": dataset
                                }

                                for dataset in DATASETS.keys()
                            ],
                            value=list(DATASETS.keys())[0],
                            clearable=False
                        )

                    ],
                    style={"width": "32%"}

                ),

                html.Div(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="country-dropdown"
                        )

                    ],
                    style={"width": "32%"}

                ),

                html.Div(

                    [
                        html.Label("Income Group"),
                        dcc.Dropdown(
                            id="income-dropdown"
                        )

                    ],

                    style={"width": "32%"}

                )

            ],

            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "20px"
            }

        ),



        html.Div(

            [

                html.Div(

                    [
                        dcc.Graph(id="country-trend")
                    ],

                    style={
                        "width": "50%"
                    }

                ),

                html.Div(

                    [
                        dcc.Graph(id="world-map")
                    ],

                    style={
                        "width": "50%"
                    }

                )

            ],

            style={
                "display": "flex"
            }

        ),


        html.Div(

            [
                html.Div(

                    [
                        dcc.Graph(
                            id="income-group-trend"
                        )
                    ],

                    style={
                        "width": "50%"
                    }

                ),

                html.Div(

                    [
                        dcc.Graph(
                            id="gender-comparison-chart"
                        )
                    ],

                    style={
                        "width": "50%"
                    }

                )

            ],

            style={
                "display": "flex"
            }

        ),

        html.Hr(),

        html.H3("Dataset Explorer"),

        dag.AgGrid(
            id="data-grid",
            defaultColDef={
                "sortable": True,
                "filter": True,
                "resizable": True
            },
            style={
                "height": "700px",
                "width": "100%"
            }

        )

    ],

    style={
        "margin": "20px",
        "fontFamily": "Segoe UI"
    }

)

# ==========================================================
# UPDATE FILTERS
# ==========================================================

@app.callback(

    Output("country-dropdown", "options"),
    Output("country-dropdown", "value"),
    Output("income-dropdown", "options"),
    Output("income-dropdown", "value"),
    Input("dataset-dropdown", "value")

)
def update_filters(dataset):

    df = DATASETS[dataset]

    countries = sorted(
        df["Country Name"]
        .dropna()
        .unique()
    )

    income_groups = sorted(
        df["IncomeGroup"]
        .dropna()
        .unique()
    )

    return (

        [
            {
                "label": country,
                "value": country
            }

            for country in countries
        ],

        countries[0],

        [
            {
                "label": income,
                "value": income
            }

            for income in income_groups
        ],
        income_groups[0]
    )

# ==========================================================
# MAIN CALLBACK
# ==========================================================

@app.callback(

    Output("country-trend", "figure"),
    Output("income-group-trend", "figure"),
    Output("gender-comparison-chart", "figure"),
    Output("world-map", "figure"),
    Output("data-grid", "rowData"),
    Output("data-grid", "columnDefs"),

    Input("dataset-dropdown", "value"),
    Input("country-dropdown", "value"),
    Input("income-dropdown", "value")

)
def update_dashboard(
        dataset,
        selected_country,
        selected_income
):

    df = DATASETS[dataset]
    year_cols = [c for c in df.columns if str(c).isdigit()]


    selected_row = df[
        df["Country Name"] == selected_country
    ]

    fig_country = px.line(
        x=year_cols,
        y=selected_row[year_cols]
        .iloc[0]
        .values,
        markers=True,
        title=f"{dataset} Trend - {selected_country}"
    )

    fig_country.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis_title=dataset

    )


    income_df = (
        pd.concat([df["IncomeGroup"],df[year_cols]], axis=1)
        .groupby("IncomeGroup")[year_cols]
        .mean()
        .T
    )

    fig_income = go.Figure()

    for group in income_df.columns:

        fig_income.add_trace(

            go.Scatter(x=income_df.index,y=income_df[group],mode="lines",
                name=group,
                opacity=(
                    1
                    if group == selected_income
                    else 0.25
                ),
                line=dict(

                    width=(
                        5
                        if group == selected_income
                        else 2
                    )
                )
            )
        )
        
    fig_income.update_layout(
        title=f"{dataset} by Income Group",
        xaxis_title="Year",
        yaxis_title=dataset,
        template="plotly_white"
    )


    fig_gender = go.Figure()
    male_country = MALE_DF[
        MALE_DF["Country Name"]
        == selected_country
    ]
    female_country = FEMALE_DF[
        FEMALE_DF["Country Name"]
        == selected_country
    ]
    if (
        not male_country.empty
        and
        not female_country.empty
    ):

        fig_gender.add_trace(
            go.Scatter(
                x=year_cols,
                y=male_country[year_cols]
                .iloc[0]
                .values,
                name="Male",
                mode="lines",
                line=dict(
                    color="blue",
                    width=3
                )

            )
        )
        fig_gender.add_trace(

            go.Scatter(
                x=year_cols,

                y=female_country[year_cols]
                .iloc[0]
                .values,
                name="Female",
                mode="lines",
                line=dict(
                    color="red",
                    width=3
                )
            )
        )

    fig_gender.update_layout(
        title=(
            f"Male vs Female "
            f"Life Expectancy - "
            f"{selected_country}"
        ),
        xaxis_title="Year",
        yaxis_title="Life Expectancy",
        hovermode="x unified",
        template="plotly_white"
    )


    fig_map = px.choropleth(

        df,

        locations="Country Code",

        locationmode="ISO-3",

        color="2023",

        hover_name="Country Name",

        color_continuous_scale="Viridis",

        title=f"{dataset} (2023)"

    )

    fig_map.update_layout(
        template="plotly_white"
    )

    table_df = df[
        df["IncomeGroup"]
        == selected_income
    ]

    row_data = table_df.to_dict(
        "records"
    )

    column_defs = [

        {
            "field": col
        }

        for col in table_df.columns

    ]

    return (

        fig_country,

        fig_income,

        fig_gender,

        fig_map,

        row_data,

        column_defs

    )


import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True)


#-------------------End of Notebook--------------------

















