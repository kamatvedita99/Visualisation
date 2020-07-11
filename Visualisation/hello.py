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
import plotly.graph_objs as go #added
import pandas as pd
import plotly.io as pio
import plotly.express as px
import nltk
import regex as re
from plotly.subplots import make_subplots




app = dash.Dash(__name__)


df1 = pd.read_csv('lock1.csv',encoding='latin')
df2 = pd.read_csv('lock2.csv',encoding='latin')
df3 = pd.read_csv('lock3.csv',encoding='latin')
df4 = pd.read_csv('lock4.csv',encoding='latin')

# Use this for hashtag extract

def hashtag_extract(x):
    hashtags = []

    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        ht=[hts.lower() for hts in ht]
        #ht=map(str.lower,ht)


        hashtags.append(ht)
    return hashtags

HT_regular = hashtag_extract(df1['tweet'][df1['labels'] == 0])
# extracting hashtags from racist/sexist tweets
HT_negative = hashtag_extract(df1['tweet'][df1['labels'] == -1])
HT_positive = hashtag_extract(df1['tweet'][df1['labels'] == 1])
# unnesting list
HT_regular = sum(HT_regular,[])
HT_negative = sum(HT_negative,[])
HT_positive = sum(HT_positive,[])
#print(HT_regular,file=sys.stderr)
#print(HT_negative,file=sys.stderr)
#positive hashtags
a = nltk.FreqDist(HT_regular)
d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})
# selecting top 10 most frequent hashtags     
d = d.nlargest(columns="Count", n = 5) 
d.head()
#plt.figure(figsize=(22,10))
#ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
#ax.set(ylabel = 'Count')
#plt.show()
#negative hastags funtion will come over here
b = nltk.FreqDist(HT_negative)
e = pd.DataFrame({'Hashtag': list(b.keys()), 'Count': list(b.values())})
# selecting top 10 most frequent hashtags
e = e.nlargest(columns="Count", n = 5)   
#plt.figure(figsize=(16,5))
#ax = sns.barplot(data=e, x= "Hashtag", y = "Count")
#ax.set(ylabel = 'Count')
#plt.show()'''
g = nltk.FreqDist(HT_positive)
h = pd.DataFrame({'Hashtag': list(g.keys()),
                  'Count': list(g.values())})
# selecting top 10 most frequent hashtags     
h = h.nlargest(columns="Count", n = 5) 
#Use this for wordcount
'''
def word_count(sentence):
    return len(sentence.split())
df['word count'] = df['text'].apply(word_count)
x = df['word count'][df.labels == 1]
y = df['word count'][df.labels == 0]
print(x,file=sys.stderr)
print(y,file=sys.stderr)
#plt.figure(figsize=(12,6))
#plt.xlim(0,45)
#plt.xlabel('word count')
#plt.ylabel('frequency')
#g = plt.hist([x, y], color=['r','b'], alpha=0.5, label=['positive','negative'])
#plt.legend(loc='upper right')
#Till here'''


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
#------------------------------------------DONUT CHART----------------------------------------------------------
count1=(df1['labels'][df1['labels']==1]).count()
countneg=(df1['labels'][df1['labels']==-1]).count()
count0=(df1['labels'][df1['labels']==0]).count()
print(count1)
colors=['#ff9595','royalblue','#80bdab']
#--------------------------------------HASHTAGS SUBPLOTS---------------------------------------------------------
fig = make_subplots(rows=1, cols=3)

fig.add_trace(
    go.Bar(y=e.Hashtag,
                x=e.Count,
                name='# Negative',
                textfont_color='white',
                
                orientation='h'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(y=h.Hashtag,
                x=h.Count,
                name='# Positive',
                textfont_color='white',
                
                orientation='h'),
    row=1, col=2
)

fig.add_trace(
    go.Bar(y=d.Hashtag,
                x=d.Count,
                name='# Neutral',
                textfont_color='white',

                orientation='h'),
    row=1, col=3
)



fig.update_layout( title ="Bar Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                uniformtext_minsize=8, 
                uniformtext_mode='hide',
                title_text="Popular Hashtags"

                )


#----------------------------------------WATSON TONE ANALYSER------------------------------------------------------------
tone=pd.read_csv('lock1ToneAnalyser.csv')
count_sad=tone['sadness'].sum()
count_joy=tone['joy'].sum()
count_confident=tone['confident'].sum()
count_analytical=tone['analytical'].sum()
count_tentative=tone['tentative'].sum()
count_fear=tone['fear'].sum()
count_anger=tone['anger'].sum()

colors_emo=['#ff9595','#ff9595','#ff9595','#80bdab','royalblue','royalblue','royalblue']

fig1 = go.Figure([go.Bar(
             x=['😁','😎','🧐','😐','🥺','😭','😡'],
             y=[count_joy,count_confident,count_analytical,count_tentative,count_sad,count_fear,count_anger],
             hovertext=['Happy','Hopeful','Analytical','Neutral','Sad','Fearful','Angry'],
             hoverinfo='text+y',
             marker_color=colors_emo
             

    )])





fig1.update_layout( title ="Bar Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                uniformtext_minsize=8, 
                uniformtext_mode='hide',
                title_text="Tone Analysis",
                #yaxis_tickformat='percent'
                )
fig1.update_xaxes(tickfont=dict(size=25))

#-------------------------------------------------LINE CHART-------------------------------------------------------------
df_p1=pd.read_csv('df_p1.csv')
df_neg1=pd.read_csv('df_neg1.csv')
df_neu1=pd.read_csv('df_neu1.csv')
fig2=go.Figure()
    
#fig2=tools.make_subplots(rows=1,cols=3,shared_xaxes=True,shared_yaxes=True)
fig2.add_trace(go.Scatter(x=df_neg1.day,
    y=df_neg1.neg,name='negatives'))
fig2.add_trace(go.Scatter(x=df_p1['day'],
    y=df_p1['pos'],name='positives'))

fig2.add_trace(go.Scatter( x=df_neu1.day,
    y=df_neu1.neu,name='neutrals'))

fig2['layout'].update( title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                #yaxis_tickformat='percent'
                )
#fig2.update_xaxes(tickfont=dict(size=5))
#----------------------------------------------CHINA-------------------------------------------------------------
d1=pd.read_csv('./China/Lock1.csv')
d2=pd.read_csv('./China/Lock2.csv')
d3=pd.read_csv('./China/Lock3.csv')
d4=pd.read_csv('./China/Lock4.csv')
china_lock1_pos=(d1['labels'][d1['labels']==1]).count()
china_lock1_neg=(d1['labels'][d1['labels']==-1]).count()
china_lock2_pos=(d2['labels'][d2['labels']==1]).count()
china_lock2_neg=(d2['labels'][d2['labels']==-1]).count()
china_lock3_pos=(d3['labels'][d3['labels']==1]).count()
china_lock3_neg=(d3['labels'][d3['labels']==-1]).count()
china_lock4_pos=(d4['labels'][d4['labels']==1]).count()
china_lock4_neg=(d4['labels'][d4['labels']==-1]).count()

lockdown=['Lockdown 1.0', 'Lockdown 2.0', 'Lockdown 3.0','Lockdown 4.0']

figchina = go.Figure(data=[
    go.Bar(name='Negative', x=lockdown,y=['0.8','0.09','0.33','0.98'],textposition='auto'),
    go.Bar(name='Positive', x=lockdown,y=['0.77','0.77','0.3','0.44'],textposition='auto')
])
# Change the bar mode
figchina.update_layout(barmode='group',
                title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                yaxis_tickformat=',.0%',
                yaxis_range=[0,1]


    )
figchina.update_yaxes(showticklabels=True)
#-------------------------------------------------------------------------------------------------------------------
#----------------------------------------------UNITY-------------------------------------------------------------
d1=pd.read_csv('./China/Lock1.csv')
d2=pd.read_csv('./China/Lock2.csv')
d3=pd.read_csv('./China/Lock3.csv')
d4=pd.read_csv('./China/Lock4.csv')
china_lock1_pos=(d1['labels'][d1['labels']==1]).count()
china_lock1_neg=(d1['labels'][d1['labels']==-1]).count()
china_lock2_pos=(d2['labels'][d2['labels']==1]).count()
china_lock2_neg=(d2['labels'][d2['labels']==-1]).count()
china_lock3_pos=(d3['labels'][d3['labels']==1]).count()
china_lock3_neg=(d3['labels'][d3['labels']==-1]).count()
china_lock4_pos=(d4['labels'][d4['labels']==1]).count()
china_lock4_neg=(d4['labels'][d4['labels']==-1]).count()

lockdown=['Lockdown 1.0', 'Lockdown 2.0', 'Lockdown 3.0','Lockdown 4.0']

figchina = go.Figure(data=[
    go.Bar(name='Negative', x=lockdown,y=['0.8','0.09','0.33','0.98'],textposition='auto'),
    go.Bar(name='Positive', x=lockdown,y=['0.77','0.77','0.3','0.44'],textposition='auto')
])
# Change the bar mode
figchina.update_layout(barmode='group',
                title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                yaxis_tickformat=',.0%',
                yaxis_range=[0,1]


    )
figchina.update_yaxes(showticklabels=True)
#-------------------------------------------------------------------------------------------------------------------
#----------------------------------------------WFH-------------------------------------------------------------
d1=pd.read_csv('./China/Lock1.csv')
d2=pd.read_csv('./China/Lock2.csv')
d3=pd.read_csv('./China/Lock3.csv')
d4=pd.read_csv('./China/Lock4.csv')
china_lock1_pos=(d1['labels'][d1['labels']==1]).count()
china_lock1_neg=(d1['labels'][d1['labels']==-1]).count()
china_lock2_pos=(d2['labels'][d2['labels']==1]).count()
china_lock2_neg=(d2['labels'][d2['labels']==-1]).count()
china_lock3_pos=(d3['labels'][d3['labels']==1]).count()
china_lock3_neg=(d3['labels'][d3['labels']==-1]).count()
china_lock4_pos=(d4['labels'][d4['labels']==1]).count()
china_lock4_neg=(d4['labels'][d4['labels']==-1]).count()

lockdown=['Lockdown 1.0', 'Lockdown 2.0', 'Lockdown 3.0','Lockdown 4.0']

figchina = go.Figure(data=[
    go.Bar(name='Negative', x=lockdown,y=['0.8','0.09','0.33','0.98'],textposition='auto'),
    go.Bar(name='Positive', x=lockdown,y=['0.77','0.77','0.3','0.44'],textposition='auto')
])
# Change the bar mode
figchina.update_layout(barmode='group',
                title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                yaxis_tickformat=',.0%',
                yaxis_range=[0,1]


    )
figchina.update_yaxes(showticklabels=True)
#-------------------------------------------------------------------------------------------------------------------
#----------------------------------------------GOVT-------------------------------------------------------------
d1=pd.read_csv('./China/Lock1.csv')
d2=pd.read_csv('./China/Lock2.csv')
d3=pd.read_csv('./China/Lock3.csv')
d4=pd.read_csv('./China/Lock4.csv')
china_lock1_pos=(d1['labels'][d1['labels']==1]).count()
china_lock1_neg=(d1['labels'][d1['labels']==-1]).count()
china_lock2_pos=(d2['labels'][d2['labels']==1]).count()
china_lock2_neg=(d2['labels'][d2['labels']==-1]).count()
china_lock3_pos=(d3['labels'][d3['labels']==1]).count()
china_lock3_neg=(d3['labels'][d3['labels']==-1]).count()
china_lock4_pos=(d4['labels'][d4['labels']==1]).count()
china_lock4_neg=(d4['labels'][d4['labels']==-1]).count()

lockdown=['Lockdown 1.0', 'Lockdown 2.0', 'Lockdown 3.0','Lockdown 4.0']

figchina = go.Figure(data=[
    go.Bar(name='Negative', x=lockdown,y=['0.8','0.09','0.33','0.98'],textposition='auto'),
    go.Bar(name='Positive', x=lockdown,y=['0.77','0.77','0.3','0.44'],textposition='auto')
])
# Change the bar mode
figchina.update_layout(barmode='group',
                title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                yaxis_tickformat=',.0%',
                yaxis_range=[0,1]


    )
figchina.update_yaxes(showticklabels=True)
#-------------------------------------------------------------------------------------------------------------------
#----------------------------------------------EXTEND-------------------------------------------------------------
d1=pd.read_csv('./China/Lock1.csv')
d2=pd.read_csv('./China/Lock2.csv')
d3=pd.read_csv('./China/Lock3.csv')
d4=pd.read_csv('./China/Lock4.csv')
china_lock1_pos=(d1['labels'][d1['labels']==1]).count()
china_lock1_neg=(d1['labels'][d1['labels']==-1]).count()
china_lock2_pos=(d2['labels'][d2['labels']==1]).count()
china_lock2_neg=(d2['labels'][d2['labels']==-1]).count()
china_lock3_pos=(d3['labels'][d3['labels']==1]).count()
china_lock3_neg=(d3['labels'][d3['labels']==-1]).count()
china_lock4_pos=(d4['labels'][d4['labels']==1]).count()
china_lock4_neg=(d4['labels'][d4['labels']==-1]).count()

lockdown=['Lockdown 1.0', 'Lockdown 2.0', 'Lockdown 3.0','Lockdown 4.0']

figchina = go.Figure(data=[
    go.Bar(name='Negative', x=lockdown,y=['0.8','0.09','0.33','0.98'],textposition='auto'),
    go.Bar(name='Positive', x=lockdown,y=['0.77','0.77','0.3','0.44'],textposition='auto')
])
# Change the bar mode
figchina.update_layout(barmode='group',
                title ="Line Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                #uniformtext_minsize=8, 
                #uniformtext_mode='hide',
                title_text="Emotional Trends in Lockdown 1.0",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False),
                yaxis_tickformat=',.0%',
                yaxis_range=[0,1]


    )
figchina.update_yaxes(showticklabels=True)
#-------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------OVERALL Sentiment-----------------------------------------------
figoverall = make_subplots(rows=1, cols=3)

figoverall.add_trace(
    go.Bar(y=[100,50,70,89],
                x=lockdown,
                name='# Negative',
                textfont_color='white',
                
                #orientation='h'
                ),
    row=1, col=1
)

figoverall.add_trace(
    go.Bar(y=[100,50,70,89],
                x=lockdown,
                name='# Positive',
                textfont_color='white',
                
                #orientation='h'
                ),
    row=1, col=2
)

figoverall.add_trace(
    go.Bar(y=[100,50,70,89],
                x=lockdown,
                name='# Neutral',
                textfont_color='white',

                #orientation='h'
                ),
    row=1, col=3
)



figoverall.update_layout( title ="Bar Chart",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a",
                plot_bgcolor="#07031a",
                uniformtext_minsize=8, 
                uniformtext_mode='hide',
                title_text="Popular Hashtags"

                )
#----------------------------------------------------------------------------------------------
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
       return html.Div([
        
html.Div([
            dcc.Graph(
            id="pie_chart",
            figure=
         {
            'data':[
            go.Pie(
                labels=['positives','negatives','neutrals'],
                hole=.8,

                values=[count1,countneg,count0],
                name="Sentiment Analysis",
                hoverinfo='label+percent',
                textinfo='label+percent',
                insidetextorientation='radial',
                textfont_color='white',
                marker=dict(colors=colors))],
            'layout':go.Layout(
                title ="Emotion Distribution",
                font=dict(
                    family="Courier New,monospace",
                    size=14,
                    color='white'

                      ),

                paper_bgcolor ="#07031a"
                )})]
            ,style={'width':'50%','display':'inline-block','padding':'0 0 0 20'}),


html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=fig1,
         )]
            ,style={'width':'50%','display':'inline-block','padding':'0 0 0 20'}),

html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=fig,
         )]
            ,style={'display':'block','padding':'0 0 0 20'}),

html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=fig2,
         )]
            ,style={'display':'block','padding':'0 0 0 20'}),


html.Div([ 
        html.Img(src=app.get_asset_url('lock1Word1.jpeg')),
        html.Img(src=app.get_asset_url('lock1Word-1.jpeg')) 

         ]

        ,style={'width':'100%','display':'block'}),





        ],style={'background':'#25274d'})
#-------------------------------------------------

        
   
        
    elif tab == 'tab-3':
       return html.Div([
        html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=figchina,
         )]
            ,style={'width':'50%','display':'inline-block','padding':'0 0 0 20'}),

        html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=figchina,
         )]
            ,style={'width':'50%','display':'inline-block','padding':'0 0 0 20'}),

       
       html.Div([
            dcc.Graph(
            id="bar_chart",
            figure=figoverall,
         )]
            ,style={'display':'block','padding':'0 0 0 20'}),
    
        
     ]),
    

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
    app.run_server(debug=True)
