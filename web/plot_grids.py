from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import data_processing as dp
import plotly.express as px
import pandas as pd


def create_daily_revenue_line_chart():

    #get dataset merging two collections orders and order details
    merged_df = dp.get_merged_df()
    # Calculate daily revenue
    #daily_revenue = dp.compute_daily_revenue(order_details_df)
    
    # Calculate daily revenue from the merged DataFrame
    daily_revenue = dp.compute_daily_revenue(merged_df)


    # Create a line chart
    fig = px.line(daily_revenue, x='OrderDate', y='LineTotal',
                labels={'OrderDate': 'Order Date', 'LineTotal': 'Gross Revenue'},
                title='Daily Gross Revenue')
    fig.update_layout(xaxis_title='Order Date', yaxis_title='Gross Revenue ($)')
    
    return fig

def create_daily_revenue_bar_chart():
    #get dataset merging two collections orders and order details
    merged_df = dp.get_merged_df()
    
    # Ensure the Order_Date column is in datetime format
    merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'])

    # Calculate daily revenue from the merged DataFrame
    daily_revenue_df = dp.compute_daily_revenue(merged_df)
    
    # Create a bar chart
    fig = px.bar(daily_revenue_df, x='OrderDate', y='LineTotal',
                 labels={'OrderDate': 'Order Date', 'LineTotal': 'Gross Revenue'},
                 title='Daily Gross Revenue')
    fig.update_layout(xaxis_title='Order Date', yaxis_title='Gross Revenue ($)', bargap=0.2)

    return fig