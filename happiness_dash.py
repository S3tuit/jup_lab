import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback

df = pd.read_csv(r'C:\Users\matte\OneDrive\Desktop\GitHub\data\happiness\clear_data.csv')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# —————————LINE
df_line = df.loc[df['Country'].isin(['Italy', 'France', 'Germany']), ['Country','Score', 'Year']]
fig_line = px.line(df_line, x='Year', y='Score', color='Country')
fig_line.update_xaxes(tickvals=list(df['Year'].unique()), ticktext=list(df['Year'].unique()))
# —————————

# —————————SCATTER 
df_scat = df.loc[df['Year'] == 2019, ['Country','Generosity', 'Rank', 'Economy strength', 'Score']]
fig_scat = px.scatter(df_scat, x='Generosity', y='Economy strength', size='Score',
                 color='Rank', hover_data=['Country', 'Rank'], color_continuous_scale= px.colors.sequential.Plasma_r,
                 labels={'Rank': '<b>Happiness <br>Rank<b>', 'Economy strength':'Economy Strength'})

fig_scat.update_traces(
    hovertemplate='<b>Country:</b> %{customdata[0]}<br><b>Happiness rank:</b> %{customdata[1]}<extra></extra>'
)
# —————————

app = Dash(__name__)

app.layout = html.Div([
    
    html.Div(children=[
    
        html.H1(children='Just a Title',
                style={
                    'textAlign':'center',
                    'color':colors['text']
                }
        ),
        
        html.Div(children='''
                Maybe 2 paragraphs.
                ''',
                style={
                    'textAlign':'center',
                    'color':colors['text']
                }
        ),
        dcc.Graph(
            id='line-fig',
            figure=fig_line
        ),
        html.Br(),

        dcc.Graph(
            id='scat-fig',
            figure=fig_scat
        ),
    ],style={'backgroundColor': colors['background']}),

    html.Div(children=[

        dcc.Graph(
        id='scat-fig',
        figure=fig_scat
        ),
    ])
])
    

if __name__ == '__main__':
    app.run(debug=True)







