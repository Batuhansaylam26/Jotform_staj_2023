import pandas as pd 



from plotly.subplots import make_subplots
import plotly.graph_objects as go

from dash import Dash,dcc, html, Input, Output, callback
from decompose import decompose
formtemplatescategories=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesCategories.csv")
dec1=decompose()
dec2=decompose()
dec3=decompose()
dec3.sd("Tax Forms","Noncovid")
fig3=dec3.figure_update()
app = Dash(__name__)
app.layout=html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                formtemplatescategories.metaKeywords.unique().tolist(),
                "Tax Forms",
                id="y1",
                searchable=True
        )
        ],style={"width":"50%",'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                ["Covid","Noncovid"],
                'Noncovid',
                id="cov1"
        )
        ],style={"width":"50%","float":"right",'display':'inline-block'})
    ],style={"width":"45%",'display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                formtemplatescategories.metaKeywords.unique().tolist(),
                "Summer Camp Evaluations",
                id="y2",
                searchable=True
        )
        ],style={"width":"50%",'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                ["Covid","Noncovid"],
                'Noncovid',
                id="cov2"
        )
        ],style={"width":"50%","float":"right",'display':'inline-block'})
    ],style={"width":"45%","float":"right",'display':'inline-block'}),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic1")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic2")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ])
        ]
    )

@callback(
    Output("plotindic1","figure"),
    Input("y1","value"),
    Input("cov1","value")
)
def update_graph(yaxis,cov):
    global dec1
    dec1.sd(yaxis,cov)
    return dec1.figure_update()
@callback(
    Output("plotindic2","figure"),
    Input("y2","value"),
    Input("cov2","value")
)
def update_graph(yaxis,cov):
    global dec2
    dec2.sd(yaxis,cov)
    return dec2.figure_update()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port='8050',debug=True)
    
