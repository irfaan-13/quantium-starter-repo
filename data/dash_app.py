import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load and prepare data
data_file = 'formatted_sales.csv'  # Adjust path if needed
df = pd.read_csv(data_file)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Clean Sales column (remove $ if any, convert to float)
df['Sales'] = df['Sales'].astype(str).str.replace(r'[\$,]', '', regex=True)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Clean Region column for consistent filtering
df['Region'] = df['Region'].astype(str).str.lower().str.strip()

# Initialize Dash app
app = Dash(__name__)

# Define region options
region_options = [
    {'label': 'All', 'value': 'all'},
    {'label': 'North', 'value': 'north'},
    {'label': 'East', 'value': 'east'},
    {'label': 'South', 'value': 'south'},
    {'label': 'West', 'value': 'west'}
]

# App layout
app.layout = html.Div(
    style={
        'maxWidth': '900px',
        'margin': 'auto',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'backgroundColor': '#f9f9f9',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
    },
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={'textAlign': 'center', 'color': '#2C3E50', 'marginBottom': '10px'}
        ),
        html.P(
            "Select a region to filter Pink Morsel sales data:",
            style={'textAlign': 'center', 'fontSize': '18px', 'color': '#34495E', 'marginBottom': '20px'}
        ),
        dcc.RadioItems(
            id='region-radio',
            options=region_options,
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '20px', 'fontSize': '16px', 'color': '#2980B9', 'cursor': 'pointer'},
            inputStyle={"marginRight": "8px"}
        ),
        dcc.Graph(id='sales-line-chart'),
        html.Div(
            "Price increase date: January 15, 2021",
            style={'textAlign': 'center', 'fontWeight': 'bold', 'marginTop': '20px', 'color': '#E74C3C', 'fontSize': '16px'}
        )
    ]
)

# Callback to update chart based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_line_chart(selected_region):
    if selected_region != 'all':
        filtered_df = df[df['Region'] == selected_region]
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        fig = px.line(title="No data available")
        fig.add_annotation(
            text="No data for selected region",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20)
        )
        return fig

    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()

    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title=f"Daily Total Sales of Pink Morsels ({selected_region.capitalize() if selected_region != 'all' else 'All Regions'})",
        labels={'Date': 'Date', 'Sales': 'Total Sales ($)'},
        height=500,
        width=900
    )

    # Add vertical line without annotation_text to avoid error
    fig.add_vline(x='2021-01-15', line_dash='dash', line_color='red')

    # Add annotation separately
    fig.add_annotation(
        x='2021-01-15',
        y=daily_sales['Sales'].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        xref='x',
        yref='y'
    )

    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
        font=dict(color='#34495E'),
        margin=dict(t=60, b=40, l=40, r=40)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
