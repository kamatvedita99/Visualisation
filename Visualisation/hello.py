#from cloudant import Cloudant #!!COMMENTED FROM BHUSHAN'S CODE!!
from flask import Flask, render_template, request, jsonify
#import atexit #!!COMMENTED FROM BHUSHAN'S CODE!!
import os
import json
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
external_stylesheets = [dbc.themes.BOOTSTRAP]
colors = {
    'background': '#000000',
    'text': '#ffffff'
}


app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
'''
db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)'''

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000

#port = int(os.getenv('PORT', 8000)) #!!COMMENTED FROM BHUSHAN'S CODE!!

#@app.route('/')
#def root():
#    return app.send_static_file('index.html')

df = pd.read_csv(r'C:\Users\VEDITA KAMAT\Desktop\VEDITA\MyProjects\IBMHC\Visualisation\final.csv')

app.layout =  html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Live Tweets', value='tab-1'),
        dcc.Tab(label='Lockdown Analysis', value='tab-2'),
        dcc.Tab(label='Lockdown 1.0', value='tab-3'),
        dcc.Tab(label='Lockdown 2.0', value='tab-4'),
        dcc.Tab(label='Lockdown 3.0', value='tab-5'),
        dcc.Tab(label='Lockdown 4.0', value='tab-6'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers',
                marker_color='cornflowerblue'

                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])
    elif tab == 'tab-2':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers'
                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])
    elif tab == 'tab-3':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers'
                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])
    elif tab == 'tab-4':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers'
                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])
    elif tab == 'tab-5':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers'
                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])
    elif tab == 'tab-6':
       return html.Div([
        dcc.Graph(
            id="scatter_chart",
            figure={
            'data':[
            go.Scatter(
                x=df.text,
                y=df.labels,
                mode='markers'
                )

            ],
            'layout':go.Layout(
                title ="Scatterplot",
                xaxis = {'title': 'Tweet'},
                yaxis = {'title': 'label'}

                )
            }


            )


        ])


# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
'''
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])'''

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
'''
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()'''
if __name__ == '__main__':
    app.run_server(port =8000,debug=True)
