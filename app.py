# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# Load the loan dataset into 'Loan_df'
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

import plotly.graph_objs as go
import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load the loan dataset into 'Loan_df'
Loan_df = pd.read_csv('C:\\Users\\HP\\Desktop\\loan_data.csv')

# Define the list of features for dropdowns
features = ['fico', 'int.rate', 'installment', 'log.annual.inc', 'dti']

colors = {
    'text': '#050498',
    'plot_color': '#E0ECFF',
    'paper_color': '#F3F2FA',
    'dropdown_option_color': '#333'  # Change this color to your preference
}

app = dash.Dash(__name__)

# Define layout for the app
app.layout = html.Div(children=[
    html.H1(children='Loan Data Visualizations', style={'font-weight': 'bold', 'color': colors['text']}),
    html.Div(children='''
        Dash: A web application framework for our data.
    ''', style={'font-weight': 'bold', 'color': colors['text']}),
    dcc.Dropdown(
        id='loan-purpose-dropdown',
        options=[{'label': purpose, 'value': purpose} for purpose in Loan_df['purpose'].unique()],
        value=Loan_df['purpose'].unique()[0],
        style={'fontWeight': 'bold', 'color': colors['dropdown_option_color']}  # Set the dropdown options to bold and change color
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(
        id='histo_chart',
        figure={
            'data': [go.Histogram(x=Loan_df['fico'], opacity=0.8,
                                  marker={"line": {"color": "#25232C", "width": 0.3}}, nbinsx=100)],
            'layout': go.Layout(title=f"Fico Distribution", xaxis={"title": "Fico (Score)", "showgrid": False},
                                yaxis={"title": "Frequency", "showgrid": False}, )
        }, style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id='histo_chart2',
        figure={
            'data': [go.Histogram(x=Loan_df['int.rate'], opacity=0.7,
                                  marker={"line": {"color": "#25232C", "width": 0.3}}, nbinsx=100)],
            'layout': go.Layout(title=f"Interest Rate Distribution",
                                xaxis={"title": "Interest Rate (Nominal)", "showgrid": False},
                                yaxis={"title": "Frequency", "showgrid": False}, )
        }, style={'width': '48%', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id='count_plot',
        figure={
            'data': [
                go.Bar(
                    x=Loan_df['purpose'].unique(),
                    y=Loan_df.groupby(['purpose', 'not.fully.paid']).size().unstack(fill_value=0).loc[:, 1],
                    name='Not Fully Paid',
                    marker=dict(color='#FF1493')
                ),
                go.Bar(
                    x=Loan_df['purpose'].unique(),
                    y=Loan_df.groupby(['purpose', 'not.fully.paid']).size().unstack(fill_value=0).loc[:, 0],
                    name='Fully Paid',
                    marker=dict(color='#800080')
                )
            ],
            'layout': go.Layout(title='Loan Purpose vs. Loan Repayment',
                                xaxis={'title': 'Loan Purpose'},
                                yaxis={'title': 'Count'},
                                barmode='group',
                                legend={'x': 0.7, 'y': 1}
                                )
        },
        style={'width': '100%', 'display': 'inline-block'}
    ),

    html.Div([]),

    html.Div([
        dcc.Dropdown(
            id='xaxis',
            options=[{'label': i.title(), 'value': i} for i in features],
            value='int.rate',
            style={'fontWeight': 'bold', 'color': colors['dropdown_option_color']}  # Set the dropdown options to bold and change color
        )
    ],
        style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='yaxis',
            options=[{'label': i.title(), 'value': i} for i in features],
            value='fico',
            style={'fontWeight': 'bold', 'color': colors['dropdown_option_color']}  # Set the dropdown options to bold and change color
        )
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='feature-graphic')
], style={'width': '96%', 'padding': 10, 'color': colors['paper_color']})


# Create bar chart for relationship between interest rate, loan purpose, and credit policy
def generate_bar_chart(selected_purpose):
    filtered_df = Loan_df[Loan_df['purpose'] == selected_purpose]
    return {
        'data': [
            go.Bar(
                x=filtered_df['purpose'],
                y=filtered_df['int.rate'],
                marker=dict(color='pink'),
                name='Interest Rate'
            ),
            go.Bar(
                x=filtered_df['purpose'],
                y=filtered_df['credit.policy'],
                marker=dict(color='purple'),
                name='Credit Policy'
            )
        ],
        'layout': {
            'title': f'Interest Rate and Credit Policy for {selected_purpose}',
            'xaxis': {'title': 'Loan Purpose'},
            'yaxis': {'title': 'Value'},
            'barmode': 'group',
            'legend': {'x': 0.7, 'y': 1}
        }
    }


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('loan-purpose-dropdown', 'value')]
)
def update_bar_chart(selected_purpose):
    return generate_bar_chart(selected_purpose)


@app.callback(
    Output('feature-graphic', 'figure'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    return {
        'data': [go.Scatter(
            x=Loan_df[xaxis_name],
            y=Loan_df[yaxis_name],
            text=Loan_df['purpose'],
            mode='markers',
            marker={
                'size': 1.2 * Loan_df['log.annual.inc'],
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
                'color': Loan_df['dti'],  # Colors based on the 'dti' column
                'colorscale': 'Viridis',  # Choose the colorscale (you can try different ones)
                'colorbar': dict(title='DTI'),  # Add a colorbar to show the scale
            }
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_name.title()},
            yaxis={'title': yaxis_name.title()},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
