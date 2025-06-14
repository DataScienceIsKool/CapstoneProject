# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

def create_dropdown():
	options = []
	options.append({'label': 'All Sites', 'value': 'ALL'})
	options.append({'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'})
	options.append({'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'})
	options.append({'label': 'KSC LC-39A', 'value': 'KSC LC-39A'})
	options.append({'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'})

	return dcc.Dropdown(id='site-dropdown', options=options, value='ALL', placeholder='Select a Launch Site here', searchable=True)

def create_slider():
    min_payload = 0
    max_payload = 10000
    return dcc.RangeSlider(id='payload-slider', min=min_payload, 
                           max=max_payload, step=1000, 
                           value=[min_payload, max_payload],
                           marks = {0: '0', 100 : '100'})

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    if entered_site == 'ALL':
        site_counts = filtered_df.groupby('Launch Site')['class'].sum()
        site_counts = site_counts.reset_index();
        return px.pie(site_counts, values='class', 
            names='Launch Site', 
            title='Successful launch counts by site')
    else:
        class_counts = filtered_df['class'].value_counts()
        class_counts = class_counts.reset_index()
        class_counts.columns = ['class', 'count']
        return px.pie(class_counts, values='count', 
            names='class', 
            title='Success / failure ratios of specific site')

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    x_col = 'Payload Mass (kg)'
    y_col = 'class'
    color_col = 'Booster Version'
    payload_col = 'Payload Mass (kg)'

    # filter by payload range
    left = filtered_df[payload_col] >= payload_range[0]
    right = filtered_df[payload_col] <= payload_range[1]
    both = left & right
    filtered_df = filtered_df[both]
    
    return px.scatter(filtered_df, x=x_col, y=y_col, color=color_col, 
                      title='Payload weight vs launch outcome')


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                create_dropdown(),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                create_slider(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
