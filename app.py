
# coding: utf-8

# In[1]:


#Final Project
#Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income). The dashboard will have two graphs:

#The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
#The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' (more here)


# In[5]:


##### Final Kathinka

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

data = pd.read_csv('nama_10_gdp_1_Data.csv', na_values = [':', 'NaN'])

data=data[~data.GEO.str.contains("Euro")]
data['GEO']=data['GEO'].replace(['Germany (until 1990 former territory of the FRG)'], 'Germany')
data['GEO']=data['GEO'].replace(['Kosovo (under United Nations Security Council Resolution 1244/99)'], 'Kosovo')
data['GEO']=data['GEO'].replace(['Former Yugoslav Republic of Macedonia, the'], 'Macedonia')

data=data.drop(columns=['Flag and Footnotes'], axis=1)
data=data.reset_index(drop=True)

data=data.rename(index=str, columns={"TIME": "Year", "GEO": "Country",'UNIT':'Unit','NA_ITEM':'Na_item','Value':'Value'})

data['Indicator'] = data['Na_item'] + ' (' + data['Unit'] + ')'


available_indicators = data['Indicator'].unique()
available_countries = data['Country'].unique()

app.layout = html.Div([
    html.Div([
        html.H1(
            children = 'Cloud Computing Final Assignment',
                style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center', 'color':'rgb(38, 69, 124)'}
            ),
             
    html.Div([
    ], 
        style = {'margin': '30px 10px 50px 10px', 'background-color': 'white', 'height': '3px'}
    ),
        
        html.H2(
            children = 'First task',
                style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
            ),
        html.Div([
            html.P(
                children = 'The first indicator:',
                style = {'font-size': 16, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'xaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            ),
            dcc.RadioItems(
                id = 'xaxis-type',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'}
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '160px'}),
        
        html.Div([
            html.P(
                children = 'The second indicator:',
                style = {'font-size': 16, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'yaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[1],
            ),
            dcc.RadioItems(
                id = 'yaxis-type',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'}
            )
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
   
    dcc.Graph(id = 'indicator-graph1'),
    
    html.Div([
        dcc.Slider(
            id = 'year--slider',
            min = data['Year'].min(),
            max = data['Year'].max(),
            value = data['Year'].max(),
            step = None,
            marks = {str(year): str(year) for year in data['Year'].unique()}
        )
    ], 
        style = {'margin' : '20px 40px'}
    ),
     
    html.Div([
    ], 
        style = {'margin': '50px 10px 50px 10px', 'background-color': 'grey', 'height': '2px'}
    ),
    
    html.Div([
        html.H2(
            children = 'Second task',
            style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
        ),
        html.Div([
            html.P(
                children = 'The country:',
                style = {'font-size': 16, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'country_name',
                options = [{'label': i, 'value': i} for i in available_countries],
                value = available_countries[0],
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '160px'}),

        html.Div([
            html.P(
                children = 'The indicator:',
                style = {'font-size': 16, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'indicator_name',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            )
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id = 'indicator-graph2'),

])

@app.callback(
    dash.dependencies.Output('indicator-graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = data[data['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x = dff[dff['Indicator'] == xaxis_column_name]['Value'],
            y = dff[dff['Indicator'] == yaxis_column_name]['Value'],
            text = dff[dff['Indicator'] == yaxis_column_name]['Country'],
            mode = 'markers',
            marker = {
                'size': 16,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            margin = {'l': 50, 'b': 50, 't': 50, 'r': 50},
            hovermode = 'closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graph2', 'figure'),
    [dash.dependencies.Input('country_name', 'value'),
     dash.dependencies.Input('indicator_name', 'value')])

def update_graph(selected_country, selected_indicator):    
    
    return {
        'data': [go.Scatter(
            x = data[(data['Country'] == selected_country) & (data['Indicator'] == selected_indicator)]['Year'].values,
            y = data[(data['Country'] == selected_country) & (data['Indicator'] == selected_indicator)]['Value'].values,
            mode = 'lines'
        )],
        'layout': go.Layout(
            yaxis = {
                'title': selected_indicator,
                'titlefont': {'size': 16},
                'type': 'linear'
            },
            margin = {'l': 50, 'b': 50, 't': 50, 'r': 50},
            hovermode = 'closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
    

