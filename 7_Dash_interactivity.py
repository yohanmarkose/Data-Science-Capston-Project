import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app = dash.Dash(__name__)
                               
app.layout =  html.Div(children=[html.H1("SpaceX Launch Records Dashboard",
                                style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
                        html.Div([
                            html.Label("All Sites"),
                            dcc.Dropdown(
                                id="site-dropdown",
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                placeholder="Select a Launch Site here",
                                value="All",
                                searchable=True,
                                style={'textAlign': 'center'}),
                            ]),
                        html.Br(),
                        html.Br(),
                        html.Div(dcc.Graph(id='success-pie-chart'), 
                                 style={'textAlign': 'center','width':'65%'}),
                        html.Br(),
                        html.Div(dcc.RangeSlider(
                            id='payload-slider',
                            min=0, max=10000, step=1000,
                            marks={i: str(i) for i in range(0, 10000, 1000)},
                            value=[0, 10000])),
                        html.Br(),
                        html.Br(),
                        html.Div(dcc.Graph(id='success-payload-scatter-chart'), 
                                 style={'textAlign': 'center','width':'85%'}),
                        ])

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby(["Launch Site"])["class"].mean().reset_index()
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_failure_counts = filtered_df['class'].value_counts().reset_index()
        success_failure_counts.columns = ['class', 'count']
        fig = px.pie(success_failure_counts, values='count', names='class', title=f'Total success launches for Site{entered_site}')
        return fig

# Scatter Graph
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    min_payload = payload_range[0]
    max_payload = payload_range[1]
    new_df = spacex_df[spacex_df['Payload Mass (kg)'].between(min_payload, max_payload)]
    if entered_site == 'ALL':
        fig = px.scatter(new_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title='Correlation between Payload mass and Success rate for all Sites', xaxis_title = 'Payload Mass (Kg)', yaxis_title='Class')
        return fig
    else:
        new_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(new_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        fig.update_layout(title=f'Correlation between Payload mass and Success rate for Site {entered_site}', xaxis_title = 'Payload Mass (Kg)', yaxis_title='Class')
        return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)