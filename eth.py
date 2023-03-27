import csv
from datetime import datetime, timedelta
import plotly.express as px
import dash
from dash import dcc,html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np

# Read the price data from the file

with open('eth_data.txt', 'r') as file:

	reader = csv.reader(file, delimiter=' ')

	data = list(reader)

dates = []
prices = []

for row in data:
	dates.append(row[1])
	prices.append(row[0])


for i in range(len(prices)):
	prices[i] = float(prices[i].replace('$', '').replace(',', ''))

app = dash.Dash(__name__)

# Define the app layout

app.layout = html.Div([ html.H1('Ethereum Price Dashboard'),
                        dcc.Graph(id="price-graph"),
                        html.Div(id="daily-report"),
                        dcc.Interval(id="update-interval", interval=5*60*1000, n_intervals=0)
                      ])


@app.callback(Output("price-graph", "figure"), [Input("update-interval", "n_intervals")])


def update_graph(n):

	df = pd.DataFrame({'prices': prices, 'dates': dates})
	print(df)

	# Convert the timestamp to a datetime object

	df["dates"] = pd.to_datetime(df["dates"])

 	# Calculate the 20-day MA
    
	df['ma20'] = df['prices'].rolling(window=20).mean()
    
  	# Create the plot

	fig = px.line(df, x="dates" , y="prices", title="Ethereum Price")
	fig.add_trace(px.line(df,x="dates",  y='ma20',color_discrete_sequence=["red"],  title>
	fig.update_layout(legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01))

return fig


   
@app.callback(Output("daily-report", "children"), [Input("update-interval", "n_intervals">


def update_report(n):
    
	# Calculate the daily volatility
	
	volatility = np.std(prices)

    	# Calculate the open and close prices

	open_price = prices[0]
	close_price = prices[-1]

      # Calculate the daily change
	
	change = close_price - open_price

	# Create the report text

	report_text = f"Open Price: ${open_price:.2f}\nClose Price: ${close_price:.2f}\nDaily>

      # Create the report component

	report = html.Div([html.H2("Daily Report"),
				html.P(report_text)])

return report


if __name__ == '__main__':
	app.run_server(host="0.0.0.0", port=8050, debug=True)
