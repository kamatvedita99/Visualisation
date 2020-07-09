from flask import Flask, render_template, request, jsonify
import os
import json
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go #added
import pandas as pd
import plotly.io as pio
import plotly.express as px
app = dash.Dash(__name__)

df1 = pd.read_csv('lock1.csv',encoding='latin')
df2 = pd.read_csv('lock2.csv',encoding='latin')
df3 = pd.read_csv('lock3.csv',encoding='latin')
df4 = pd.read_csv('lock4.csv',encoding='latin')


app.layout =  html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Live Tweets', value='tab-1'),
        dcc.Tab(label='Lockdown Analysis', value='tab-2'),
        dcc.Tab(label='Lockdown 1.0', value='tab-3'),
        dcc.Tab(label='Lockdown 2.0', value='tab-4'),
        dcc.Tab(label='Lockdown 3.0', value='tab-5'),
        dcc.Tab(label='Lockdown 4.0', value='tab-6'),
    ],
      colors={
                "border":"#eeeeee",
                "primary":"#679b9b",
                "background":"#2e9cc8",

      }
    ),
    html.Div(id='tabs-content')
])

count1=(df1['labels'][df1['labels']==1]).count()
countneg=(df1['labels'][df1['labels']==-1]).count()
count0=(df1['labels'][df1['labels']==0]).count()

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="start",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="end",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), align="start"),
                dbc.Col(html.Div("One of three columns"), align="center"),
                dbc.Col(html.Div("One of three columns"), align="end"),
            ]
        ),
    ]
)

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
#fig.show()

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
	

    if tab == 'tab-1':
       return html.Div([
       	html.Div([
       		fig.show()
       		],style={'width':'33.33%','display':'inline-block','padding':'0 0 0 20'})],

       	style={'background':'#25274d'})

if __name__ == '__main__':
    app.run_server(port =8000,debug=True)

