import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('avocado.csv')

# Create a bar chart function
def create_bar_chart(df, selected_region, selected_year):
    if selected_region == 'All Regions':
        filtered_df = df[df['year'] == selected_year]
        title = f'Average Price for All Regions in {selected_year}'
    else:
        filtered_df = df[(df['region'] == selected_region) & (df['year'] == selected_year)]
        title = f'Average Price in {selected_region} for {selected_year}'
    fig = px.bar(filtered_df, x='region', y='AveragePrice', title=title)
    return fig

# Create a choropleth map function
def create_choropleth_map(df, selected_year):
    filtered_df = df[df['year'] == selected_year]
    fig = px.choropleth(
        filtered_df,
        locations='region',
        locationmode='USA-states',
        color='AveragePrice',
        color_continuous_scale='Viridis',
        title=f'Average Price per Region in {selected_year}',
        scope='usa'
    )
    return fig

# Create the Dash app
app = dash.Dash(__name__)

# Define unique regions and years for dropdown options
regions = list(df['region'].unique())
regions.append('All Regions')  # Add the option for All Regions
years = df['year'].unique()

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Avocado Prices'),

    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in regions],
        value=regions[0],  # Set the default value to the first region
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in years],
        value=years[0],  # Set the default value to the first year
        multi=False,
        style={'width': '50%'}
    ),

    dcc.Graph(
        id='bar-chart',
    ),

    dcc.Graph(
        id='choropleth-map',
    )
])

# Define callbacks to update charts based on dropdown selections
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_bar_chart(selected_region, selected_year):
    return create_bar_chart(df, selected_region, selected_year)

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_choropleth_map(selected_year):
    return create_choropleth_map(df, selected_year)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
