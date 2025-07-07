import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load data
df = pd.read_csv('formatted_sales.csv')
# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Clean Sales column: remove $ and convert to float
df['Sales'] = df['Sales'].astype(str).str.replace(r'[\$,]', '', regex=True).astype(float)

# Group by date and sum sales
daily_sales = df.groupby('Date')['Sales'].sum().reset_index()
print(daily_sales.head())  # Debug: check your data!

# Create line chart
fig = px.line(
    daily_sales,
    x='Date',
    y='Sales',
    title='Daily Total Sales of Pink Morsels',
    labels={'Date': 'Date', 'Sales': 'Total Sales ($)'},
    height=500,
    width=900
)
fig.add_vline(x='2021-01-15', line_dash='dash', line_color='red')
fig.add_annotation(
    x='2021-01-15',
    y=daily_sales['Sales'].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Soul Foods Pink Morsel Sales Visualiser'),
    html.P('Visualising sales before and after the price increase on January 15, 2021'),
    dcc.Graph(figure=fig),
    html.Div([
        html.P("Price increase date: January 15, 2021", style={'fontWeight': 'bold', 'marginTop': '20px'})
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
