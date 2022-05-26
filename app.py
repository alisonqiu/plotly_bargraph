import os
import plotly.express as px
from dash import Input, Output, callback, dash_table,State
import pandas as pd
import requests
import json
from app_secrets import *
from app_secrets import *
import dash
from dash import dcc
from dash import html



bar_x_vars=[
	'voyage_ship__imputed_nationality__name',
	'voyage_ship__rig_of_vessel__name',
	'voyage_outcome__particular_outcome__name',
	'voyage_outcome__outcome_slaves__name',
	'voyage_outcome__outcome_owner__name',
	'voyage_outcome__vessel_captured_outcome__name',
	'voyage_outcome__resistance__name',
	'voyage_itinerary__imp_port_voyage_begin__place',
	'voyage_itinerary__imp_region_voyage_begin__region',
	'voyage_itinerary__imp_principal_place_of_slave_purchase__place',
	'voyage_itinerary__imp_principal_region_of_slave_purchase__region',
	'voyage_itinerary__imp_principal_port_slave_dis__place',
	'voyage_itinerary__imp_principal_region_slave_dis__region',
	'voyage_itinerary__imp_broad_region_slave_dis__broad_region',
	'voyage_itinerary__place_voyage_ended__place',
	'voyage_itinerary__region_of_return__region',
	'voyage_dates__imp_arrival_at_port_of_dis_yyyy',
	'voyage_dates__voyage_began_mm',
	'voyage_dates__slave_purchase_began_mm',
	'voyage_dates__date_departed_africa_mm',
	'voyage_dates__first_dis_of_slaves_mm',
	'voyage_dates__voyage_completed_mm'
]

bar_y_abs_vars=[
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_dates__length_middle_passage_days',	
	'voyage_ship__tonnage_mod',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',					
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
	'voyage_slaves_numbers__imp_jamaican_cash_price'
	]

app = dash.Dash()
server = app.server

app.layout = html.Div([
    dcc.Dropdown(
    id='bar_x_var',
    options=[i for i in bar_x_vars],
    value='voyage_ship__rig_of_vessel__name',
    multi=False
),
dcc.Dropdown(
    id='bar_y_var',
    options=[i for i in bar_y_abs_vars],
    value='voyage_dates__imp_length_home_to_disembark',
    multi=False
),    
    dcc.Graph(id='fizz')
])

@app.callback(
Output('fizz', 'figure'),
Input('bar_x_var', 'value'),
Input('bar_y_var', 'value')
    
)
def update_bar_graph(bar_x_var,bar_y_var):
	global headers
	print("headers",headers)
	data={
	'selected_fields':[bar_x_var,bar_y_var],
	'cachename':['voyage_bar_and_donut_charts']
	}

	url="https://voyages3-api.crc.rice.edu/voyage/caches"

	r=requests.post(url,data=data,headers=headers)
	#print("data",data)

	#print(r)
	j=r.text
	#print(j)

	df=pd.read_json(j)
	print(df)
	df = df.groupby([bar_x_var, # combines data for duplicate geo and date vars. 
	
				], as_index=False).sum()
	print(bar_x_var,bar_y_var)
	fig=px.bar(df,x=bar_x_var,y=bar_y_var,
	labels={
	bar_y_var:'yvarlabel',
	bar_x_var:'xvarlabel'
	}
	)
	return fig


if __name__ == '__main__':
	app.run_server(debug=False)
