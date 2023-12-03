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


drop_line = list(df['Country'].unique())
drop_line.append('World')

radio_y = list(df['Year'].unique())
radio_f = ['Family', 'Generosity', 'Perceived freedom', 'Trust in the gov', 'Generosity']

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
            id='scat-fig'
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

        html.H2('Year Selection'

        ),

        dcc.RadioItems(radio_y, value=2019,
                     inline=True, id='radio_y'
        ),

        html.H2('Property Selection'

        ),

        dcc.RadioItems(radio_f, value='Family',
                     inline=True, id='radio_f'
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
        id='scat2-fig'
        ),
        html.Br(),
    
        dcc.Graph(
            id='chf-fig'
        ),

        html.Br(),
        
        dcc.Graph(
        id='chh-fig'
        ),
        html.Br(),

    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'row'})

@callback(
    Output(component_id='line-fig', component_property='figure'),
    Output(component_id='scat-fig', component_property='figure'),
    Output(component_id='scat2-fig', component_property='figure'),
    Output(component_id='chf-fig', component_property='figure'),
    Output(component_id='chh-fig', component_property='figure'),
    Input(component_id='drop_line', component_property='value'),
    Input(component_id='radio_y', component_property='value'),
    Input(component_id='radio_f', component_property='value'),
)
def update_fig(drop_line_value, radio_y_value, radio_f_value):

    # —————————LINE
    if isinstance(drop_line_value, str):
        drop_line_value = [drop_line_value]

    fig_line = px.line(df.loc[df['Country'].isin(drop_line_value),:],
                       x='Year', y='Score', color='Country')
    fig_line.update_xaxes(tickvals=list(df['Year'].unique()), ticktext=list(df['Year'].unique()))
    # —————————

    # —————————SCATTER 
    df_scat = df.loc[df['Year'] == radio_y_value, :]
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
    fig_scat2 = px.scatter(df_scat, x='Life Expectancy', y='Trust in the gov', size='Rank2',
                    color='Rank', color_continuous_scale= px.colors.sequential.Plasma_r,
                    hover_data=['Country', 'Rank'],
                    labels={'Rank': '<b>Happiness <br>Rank<b>', 'Trust in the gov':'Trust in The Government'}
                    )

    fig_scat2.update_traces(
    hovertemplate='<b>Country:</b> %{customdata[0]}<br><b>Happiness rank:</b> %{customdata[1]}<extra></extra>'
    )
    # —————————
    #—————————CHORO VARIABLE
    fig_chf = px.choropleth(
        df_scat,
        locations='ISO',
        color=radio_f_value,
        hover_name='Country',
        color_continuous_scale='Emrld_r',
        labels={'Family': 'Family'},
    )
    fig_chf.update_layout(
        coloraxis_colorbar=dict(
            lenmode='pixels',
            len=350, 
            yanchor='top',
            y=1,
        )
    )
    # —————————

    #—————————CHORO HAPPY
    fig_chh = px.choropleth(
        df_scat,
        locations='ISO',
        color='Score',
        hover_name='Country',
        color_continuous_scale='Oryel_r',
        labels={'Score': 'Happiness'},
    )
    fig_chh.update_layout(
        coloraxis_colorbar=dict(
            lenmode='pixels',
            len=350, 
            yanchor='top',
            y=1,
        )
    )
    
    # —————————

    return fig_line, fig_scat, fig_scat2, fig_chf, fig_chh

if __name__ == '__main__':
    app.run(debug=True)







