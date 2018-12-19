
# coding: utf-8

# In[15]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('/Users/kathinkadekuyper/Downloads/nama_10_gdp/nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])


# In[11]:


available_indicators = df['NA_ITEM'].unique()
available_units = df['UNIT'].unique()
available_geos = df['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.H2(children='Select Measurement Unit'),
            dcc.Dropdown(
                id='unit',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )]),

        html.Div([
            html.H2(children='Select First Indicator'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.H2(children='Select Second Indicator'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Imports of goods and services'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thick black solid',
        'backgroundColor': 'rgb(255, 175, 181)',
        'padding': '5px 3px'
    }),

    html.Div([
        dcc.Graph(
            id='indicator-scatter',
            hoverData={'points': [{'customdata': 'Spain'}]}
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),    
    
    html.Div(dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}

    ), style={'width': '100%', 'padding': '10px 20px 20px 20px'}),
    
    html.Div([
        dcc.Graph(id='x-time-series')
    ], style={'display': 'inline-block', 'width': '99%'}),
    
   

])


@app.callback(
    dash.dependencies.Output('indicator-scatter', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('unit', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value, unit_value):
    dff = df[df['TIME'] == year_value]
    dff = dff[dff['UNIT'] == unit_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            customdata=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 50,
                'opacity': 0.7,
                'color' : 'rgba(152, 0, 0, .8)',
                'line': {'width': 1.0, 'color': 'black'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['TIME'],
            y=dff['Value'],
            mode='lines+markers',
            marker={
            'size': 10,
            'color': 'rgba(152, 0, 0, .8)',
            'line': {'width': 3.0, 'color': 'black'}
            }
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 175, 181, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': True}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('indicator-scatter', 'hoverData'),
     dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('unit', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type, unit_value):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['GEO'] == country_name]
    dff = dff[dff['UNIT'] == unit_value]
    dff = dff[dff['NA_ITEM'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)



if __name__ == '__main__':
    app.run_server()


# In[12]:





# In[16]:




