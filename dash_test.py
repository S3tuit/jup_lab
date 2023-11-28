from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv(r'C:\Users\matte\OneDrive\Desktop\GitHub\data\births.csv')
df = df.loc[df['year'].isin([1973,1974,1975]), :]
df.head()


app.layout = html.Div([

    html.H1('First Dashboard with Dash—',
            style={'text-align':'center'}),

    dcc.Dropdown(id='syear',
                 options=[
                     {'label':'Mille-novecento-settanta-tre', 'value':1973},
                     {'label':'Mille-novecento-settanta-quattro', 'value':1974},
                     {'label':'Mille-novecento-settanta-cinque', 'value':1975}],
                 multi=False,
                 value=1974,
                 style={'didth':'40%'}
    ),

    html.Div(id='output_c', children=[]),
    html.Br(),

    dcc.Graph(id='birth_map', figure={})

])


@app.callback(
    [Output(component_id='output_c', component_property='children'),
    Output(component_id='birth_map', component_property='figure')],
    [Input(component_id='syear', component_property='value')]
)
def birth_map(user_inp):
    
    container = f'You choose {user_inp}'

    df2 = df.copy()
    df2 = df2[df2['month'] == 11]
    df2 = df2[df2['year'] == user_inp]

    figg = px.line(df2, x='day', y='births', color='gender')

    return container, figg

if __name__ == '__main__':
    app.run(debug=True)