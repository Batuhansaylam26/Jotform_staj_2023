import pandas as pd 



from dash import Dash,dcc, html, Input, Output, callback
from decompose import decompose
app = Dash(__name__)
formtemplatescategories=pd.read_csv("/home/batuhan-saylam/Desktop/JotformProject/formTemplatesCategories.csv")
dec1=decompose()
dec2=decompose()
dec3=decompose()
dec4=decompose()
dec=decompose()


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
        ]),
    html.Div([
        html.Div([
            dcc.Dropdown(
                formtemplatescategories.metaKeywords.unique().tolist(),
                "Virtual Event Forms",
                id="y3",
                searchable=True
        )
        ],style={"width":"50%",'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                ["Covid","Noncovid"],
                'Noncovid',
                id="cov3"
        )
        ],style={"width":"50%","float":"right",'display':'inline-block'})
    ],style={"width":"45%",'display':'inline-block'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                formtemplatescategories.metaKeywords.unique().tolist(),
                "Event Feedback Forms",
                id="y4",
                searchable=True
        )
        ],style={"width":"50%",'display':'inline-block'}),
        html.Div([
            dcc.Dropdown(
                ["Covid","Noncovid"],
                'Noncovid',
                id="cov4"
        )
        ],style={"width":"50%","float":"right",'display':'inline-block'})
    ],style={"width":"45%","float":"right",'display':'inline-block'}),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(id="plotindic3")],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(id="plotindic4")],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(figure=dec.sd("Event Evaluation Forms","Noncovid"))],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(figure=dec.sd("Event Planner Forms","Noncovid"))],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(figure=dec.sd("Event Registration Forms","Noncovid"))],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(figure=dec.sd("Event Booking","Noncovid"))],style={"width":"50%","float":"right",'display':'inline-block'}

        )
        ]),
    html.Div(
        [
        html.Div(
            
            [dcc.Graph(figure=dec.sd("Gaming Forms","Noncovid"))],style={"width":"50%",'display':'inline-block'}
            
        ),
        html.Div(
            [dcc.Graph(figure=dec.sd("Telecommuting Forms","Noncovid"))],style={"width":"50%","float":"right",'display':'inline-block'}

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
    return dec1.sd(yaxis,cov)
@callback(
    Output("plotindic2","figure"),
    Input("y2","value"),
    Input("cov2","value")
)
def update_graph(yaxis,cov):
    global dec2
    return dec2.sd(yaxis,cov)
@callback(
    Output("plotindic3","figure"),
    Input("y3","value"),
    Input("cov3","value")
)
def update_graph(yaxis,cov):
    global dec3
    return dec3.sd(yaxis,cov)
@callback(
    Output("plotindic4","figure"),
    Input("y4","value"),
    Input("cov4","value")
)
def update_graph(yaxis,cov):
    global dec4
    return dec4.sd(yaxis,cov)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port='8051',debug=False)
    
