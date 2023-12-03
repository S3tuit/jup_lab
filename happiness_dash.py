import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback

df = pd.read_csv(r'C:\Users\matte\OneDrive\Desktop\GitHub\jupyter_storytelling\Data\clear_data.csv')
for i in list(df['Year'].unique()):
    dfy = df.loc[df['Year']==i,'Score':'Family'] 
    wdata = {}
    for c in dfy.columns.to_list():
        wdata[f'{c}'] = dfy[f'{c}'].mean()
    wdata['Year'] = i
    wdata['Country'] = 'World'
    df = df._append(wdata, ignore_index=True)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#—————————CHORO FAMILY
df_chf = df.loc[df['Year']==2015, ['ISO','Family','Country']]

fig_chf = px.choropleth(
    df_chf,
    locations='ISO',
    color='Family',
    hover_name='Country',
    color_continuous_scale='Emrld_r',
    labels={'Family': 'Family'},
)

fig_chf.update_layout(
    width=720,
    height=400,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': '<b>Family Score by Country</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='#525252',
    title_font_size=33,
    font=dict(
        family='Heebo', 
        size=18, 
        color='#525252'
    ),
    margin={"r": 0, "t": 50, "l": 10, "b": 0}
    )
# —————————

#—————————CHORO HAPPY
df_chh = df.loc[df['Year']==2015, ['ISO','Score','Country']]

fig_chh = px.choropleth(
    df_chh,
    locations='ISO',
    color='Score',
    hover_name='Country',
    color_continuous_scale='Oryel_r',
    labels={'Score': 'Happiness'},
    title='Happiness Choropleth Map',
)

fig_chh.update_layout(
    width=720,
    height=400,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    title={
        'text': '<b>Happiness Score by Country</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    },
    title_font_color='#525252',
    title_font_size=33,
    font=dict(
        family='Heebo', 
        size=18, 
        color='#525252'
    ),
    margin={"r": 0, "t": 50, "l": 10, "b": 0}
    )
# —————————

# —————————SCATTER 
df_scat = df.loc[df['Year'] == 2019, ['Country','Generosity', 'Rank', 'Economy strength', 'Score']]
df_scat = df_scat[df_scat['Country'] != 'World']
df_scat['Rank2'] = df_scat['Rank'].max() - df_scat['Rank'] + 1

fig_scat = px.scatter(df_scat, x='Generosity', y='Economy strength', size='Rank2',
                 color='Rank', hover_data=['Country', 'Rank'], color_continuous_scale= px.colors.sequential.Plasma_r,
                 labels={'Rank': '<b>Happiness <br>Rank<b>', 'Economy strength':'Economy Strength'})

fig_scat.update_traces(
    hovertemplate='<b>Country:</b> %{customdata[0]}<br><b>Happiness rank:</b> %{customdata[1]}<extra></extra>'
)
# —————————

# —————————SCATTER 2
df_scat2 = df.loc[df['Year'] == 2019, ['Country','Life Expectancy', 'Rank', 'Trust in the gov', 'Score']]
df_scat2 = df_scat2[df_scat2['Country'] != 'World']
df_scat2['Rank2'] = df_scat2['Rank'].max() - df_scat2['Rank'] + 1

fig_scat2 = px.scatter(df_scat2, x='Life Expectancy', y='Trust in the gov', size='Rank2',
                 color='Rank', color_continuous_scale= px.colors.sequential.Plasma_r,
                 hover_data=['Country', 'Rank'],
                 labels={'Rank': '<b>Happiness <br>Rank<b>', 'Trust in the gov':'Trust in The Government'}
                 )

fig_scat2.update_traces(
   hovertemplate='<b>Country:</b> %{customdata[0]}<br><b>Happiness rank:</b> %{customdata[1]}<extra></extra>'
)
# —————————

drop_line = list(df['Country'].unique())
drop_line.append('World')

radio_gov = ['Life Expectancy','Perceived freedom', 'Score', 'Economy strength']

radio_eco = ['Generosity', 'Score', 'Perceived freedom']


app = Dash(__name__)

app.layout = html.Div([

# —————————COLUMN 1
    html.Div(children=[
    
        html.H1(children='Just a Title',
                style={
                    'textAlign':'Left',
                    'color':colors['text']
                }
        ),
        
        html.Div(children='''
                Maybe 2 paragraphs.
                ''',
                style={
                    'textAlign':'Left',
                    'color':colors['text']
                }
        ),
        html.Br(),
    
        dcc.Graph(
            id='line-fig',
        ),
        html.Br(),
    
        dcc.Graph(
            id='scat-fig',
            figure=fig_scat
        ),
    ],style={'backgroundColor': colors['background'],
             'padding': 10, 'flex': 1}),

# —————————COLUMN 2
    html.Div(children=[

        html.H2('Happiness Over Time'

        ),

        dcc.Dropdown(drop_line, value='World',
                     multi=True, id='drop_line'
        ),

        html.H2('Trust in The Gov vs.'

        ),

        dcc.RadioItems(radio_gov, value='Life Expectancy',
                     inline=True, id='radio_gov'
        ),

        html.H2('Economy Strength vs.'

        ),

        dcc.RadioItems(radio_eco, value='Generosity',
                     inline=True, id='radio_eco'
        ),

        html.H1(children='',
                style={
                    'textAlign':'Left',
                    'color':colors['text']
                }
        ),
        
        html.Div(children='''
                
                ''',
                style={
                    'textAlign':'Left',
                    'color':colors['text']
                }
        ),
        html.Br(),
        html.Br(),
        
        dcc.Graph(
        id='scat2-fig',
        figure=fig_scat2
        ),
        html.Br(),
    
        dcc.Graph(
            id='chf-fig',
            figure=fig_chf
        ),

        html.Br(),
        
        dcc.Graph(
        id='chh-fig',
        figure=fig_chh
        ),
        html.Br(),

    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'row'})

@callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='drop_line', component_property='value')
)
def update_fig(drop_line_value):

    # —————————LINE
    if type(drop_line_value) != 'list':
        listd = []
        listd.append(drop_line_value)
        drop_line_value = listd

    fig_line = px.line(df.loc[df['Country'].isin(drop_line_value),:],
                       x='Year', y='Score', color='Country')
    fig_line.update_xaxes(tickvals=list(df['Year'].unique()), ticktext=list(df['Year'].unique()))
    # —————————

    return fig_line

if __name__ == '__main__':
    app.run(debug=True)







