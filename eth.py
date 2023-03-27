import csv
from datetime import datetime, timedelta
import plotly.express as px
import dash
from dash import dcc,html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np

# Read the price data from the file

with open('eth.txt', 'r') as file:
    reader = csv.reader(file, delimiter=' ')
    data = list(reader)
   
with open('date.txt', 'r') as f:
    reader = csv.reader(f, delimiter=' ') 
    date = list(reader)


app = dash.Dash(__name__)

# Define the app layout

app.layout = html.Div([
  html.H1('Ethereum Price Dashboard'),
  dcc.Graph(id="price-graph"),
  html.Div(id="daily-report"),
  dcc.Interval(id="update-interval", interval=5*60*1000, n_intervals=0)
])

@app.callback(Output("price-graph", "figure"), [Input("update-interval", "n_intervals")])

def update_graph(n):
    df = pd.read_csv("eth.txt", names=["price"], header=None, sep="\t")
    df2 = pd.read_csv("date.txt", names=["dates"], header=None, sep="\t")

    # Convert the timestamp to a datetime object
    df2["dates"] = pd.to_datetime(df2["dates"])

    # Calculate the 20-day MA
    df = df.replace('[\$,]', '', regex=True).astype(float)
    df['ma20'] = df['price'].rolling(window=20).mean()

    # Create the plot
    fig = px.line(df, x=df2["dates"] , y=df["price"], title="Ethereum Price")
    fig.add_trace(px.line(df,x=df2["dates"],  y='ma20',color_discrete_sequence=["red"],  title="Moving Average 20-Days").data[0])
    fig.update_layout(legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01))

    return fig
  
  
@app.callback(Output("daily-report", "children"), [Input("update-interval", "n_intervals")])

def update_report(n):
    with open('eth.txt', 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        data = list(reader)

    # Convert the data to floats
    prices = [row[1] for row in data]
 
    for i in range(len(prices)):
        prices[i] = float(prices[i].replace('$', '').replace(',', ''))
        
    # Calculate the daily volatility
    volatility = np.std(prices)
    
    # Calculate the open and close prices
    open_price = prices[0]
    close_price = prices[-1]

    # Calculate the daily change
    change = close_price - open_price

    # Create the report text
    report_text = f"Open Price: ${open_price:.2f}\nClose Price: ${close_price:.2f}\nDaily Change: ${change:.2f}\nDaily Volatility: ${volatility:.2f}"
    
    # Create the report component
    report = html.Div([html.H2("Daily Report"), html.P(report_text)])

    return report


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
