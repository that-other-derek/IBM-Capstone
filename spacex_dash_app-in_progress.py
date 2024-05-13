# Import required libraries
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
#print('min payload is ',min_payload)
#launch site list
launch_sites = spacex_df['Launch Site'].unique()
launch_sites_all = "('" + "','".join(launch_sites) + "')"
#print(launch_sites) launch_sites_all = ', '.join(launch_sites) ('CCAFS LC-40','VAFB SLC-4E','KSC LC-39A','CCAFS SLC-40')
launch_list =[i for i in (launch_sites)]

#some task work
#success_df = spacex_df.groupby('Launch Site')[spacex_df['class']==1].sum().to_frame().reset_index()
success_df = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].sum().to_frame().reset_index()

my_values=success_df['class']
my_names=success_df['Launch Site']
#print(success_df.values)

#some task work
payload_class = spacex_df['class']
payload_wt =spacex_df['Payload Mass (kg)']

#my_values=success_df['class']
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard02',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Label('Select Launch Site'),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value':launch_sites_all}]+
                                        [{'label': i, 'value':i} for i in launch_list
                                        ],
                                    value='default',
                                    placeholder='Select A Launch Site'
                                ),
                                html.Br(),
                                html.Div(

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                
                                    dcc.Graph(
                                        id='success-pie-chart',
                                        figure=px.pie(
                                            success_df,
                                            values=my_values,
                                            names=my_names,
                                            title='Successful Launches'
                                            
                                            )
                                        )
                                )
                                    ,
                                html.Br(),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P("Payload range (Kg):"),
                                html.Div(
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min= 0, 
                                        max= 10000,
                                        step=1000,
                                        value=[min_payload,max_payload]
                                        )
                                        ),
                                
 
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(
                                        id='success-payload-scatter-chart',
                                        figure=px.scatter(
                                            spacex_df,
                                            x=payload_wt, 
                                            y=payload_class,
                                            color="Booster Version Category",
                                            title="Payload to Launch Success Correlation"
                                            ).update_layout(
                                                xaxis_title="Payload Weight (kg)",
                                                yaxis_title="Success (1) / Failure (0)"
                                                )
                                        )),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
    )
def update_output_pie(selected_site):
    # Print launch_sites_all and launch_list to the terminal
    #print('Launch sites all:', launch_sites_all)
    #print('Launch list:', launch_list)
    #print('values are: ',my_values)
    #print("Names:", my_names)
    #site_df = spacex_df[spacex_df['Launch Site'] == selected_site][['Launch Site', 'class']].reset_index(drop=True)
    #site_values=site_df['class']
    #site_names=site_df["Launch Site"]
    #print("Names2:", site_names)
    #print("values2:", site_values)



    if selected_site is None:
        return px.pie(
            success_df,
            values=my_values,
            names=my_names,
            title='Succesful Launches Initial2'
        ) 
    elif selected_site == 'default':
       # print('default')
        #print(success_df.head())
        return px.pie(
            success_df,
            
            values=my_values,
            names=my_names,
            title='Succesful Launches Initial1'
        )
    
    elif selected_site == launch_sites_all:
       # print('default')
        #print(success_df.head())
        return px.pie(
            success_df,
            
            values=my_values,
            names=my_names,
            title='Succesful Launches Initial4'
        )
    else:
       # print('selected site is: ', selected_site)
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = site_df[site_df['class']==1].shape[0]
        failure_count = site_df[site_df['class']==0].shape[0]
        #print(site_df.head())
            
        #site_values=site_df['class']
        #site_names=site_df["Launch Site"]
        

        return px.pie(
            #site_df,
            names=['Success','Failure'],
            values=[success_count,failure_count],
            
            title=f'Succesful Launches Initial3 {selected_site}'
            )
            
          


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')
    )
def update_scatter(selected_site,selected_range):
    #print('the selected range is: ',selected_range)
    if selected_site is None:
        range_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_range[0]) & (spacex_df['Payload Mass (kg)']<=selected_range[1])]
        payload_class = range_df['class']
        payload_wt =range_df['Payload Mass (kg)']

        return px.scatter(
            range_df,
            x=payload_wt, 
            y=payload_class,
            color="Booster Version Category",
            title="Payload to Launch Success Correlation 01"
            ).update_layout(
                xaxis_title="Payload Weight (kg)",
                yaxis_title="Success (1) / Failure (0)"
            )
        
    elif selected_site == 'default':
       # print('default')
        #print(success_df.head())
        range_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_range[0]) & (spacex_df['Payload Mass (kg)']<=selected_range[1])]
        payload_class = range_df['class']
        payload_wt =range_df['Payload Mass (kg)']
        return px.scatter(
            range_df,
            x=payload_wt, 
            y=payload_class,
            color="Booster Version Category",
            title="Payload to Launch Success Correlation 02"
            ).update_layout(
                xaxis_title="Payload Weight (kg)",
                yaxis_title="Success (1) / Failure (0)"
            )
    
    elif selected_site == launch_sites_all:
       # print('default')
        #print(success_df.head())
        range_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_range[0]) & (spacex_df['Payload Mass (kg)']<=selected_range[1])]
        payload_class = range_df['class']
        payload_wt =range_df['Payload Mass (kg)']

        #print('range')
        range_df.head()
        return px.scatter(
            range_df,
            x=payload_wt, 
            y=payload_class,
            color="Booster Version Category",
            title="Payload to Launch Success Correlation 03"
            ).update_layout(
                xaxis_title="Payload Weight (kg)",
                yaxis_title="Success (1) / Failure (0)"
            )
    else:
        #print('selected site is: ', selected_site)
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        range_df = site_df[(site_df['Payload Mass (kg)']>=selected_range[0]) & (site_df['Payload Mass (kg)']<=selected_range[1])]

        payload_class = range_df['class']
        payload_wt =range_df['Payload Mass (kg)']
        #print(range_df.head())    
        #site_values=site_df['class']
        #site_names=site_df["Launch Site"]
        

        return px.scatter(
            range_df,
            x=payload_wt, 
            y=payload_class,
            color="Booster Version Category",
            title=f'{selected_site} Payload to Launch Success Correlation'
            ).update_layout(
                xaxis_title="Payload Weight (kg)",
                yaxis_title="Success (1) / Failure (0)"
            )    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
