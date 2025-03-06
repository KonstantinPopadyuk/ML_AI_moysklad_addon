from typing import Literal, Dict, Any
import pandas as pd
from transformed_data import ProcessedData
import numpy as np

TimeperiodType = Literal["day", "week", "month", "year"]

class Reports:
    """
    A class to generate various analytical reports from processed sales data.
    
    This class provides methods to analyze sales data across different dimensions
    such as company types, agents, product types, volumes, and cities.
    
    Attributes:
        df (ProcessedData): Processed sales data instance
    """

    def __init__(self, df: ProcessedData):
        """
        Initialize Reports with processed data.

        Args:
            df (ProcessedData): An instance of ProcessedData containing the processed sales information
        """
        self.df = df

    def get_agents_type_report(self, period: TimeperiodType) -> pd.DataFrame:
        """
        Generate a report analyzing sales by company type.

        Args:
            period (TimeperiodType): Time period for the report ("day", "week", "month", "year")

        Returns:
            pd.DataFrame: Report containing the following columns:
                - companyType: Type of company
                - orders_count: Number of orders
                - item_mean_price: Average price per item
                - order_mean_sum: Average order value
                - orders_total_sum: Total sales value
                
        Example:
            >>> reports = Reports(processed_data)
            >>> company_report = reports.get_agents_type_report("month")
        """
        df = self.df.get_prepocessdata_slice(period)
        report = df.groupby('companyType')\
                    .agg({
                        'order_id': [('orders_count', 'count')],
                        'price': [('item_mean_price', 'mean')],
                        'sum': [('order_mean_sum', 'mean'), 
                               ('orders_total_sum', 'sum')]})\
                    .sort_values(('order_id', 'orders_count'), ascending=False)\
                    .reset_index()
        
        report.columns = ['companyType', 'orders_count', 'item_mean_price', 
                         'order_mean_sum', 'orders_total_sum']
        
        return report.round(2)
    
    def get_agents_name_report(self, period: TimeperiodType) -> pd.DataFrame:
        """
        Generate a report analyzing sales by individual agents/customers.

        Args:
            period (TimeperiodType): Time period for the report ("day", "week", "month", "year")

        Returns:
            pd.DataFrame: Report containing the following columns:
                - agent_name: Name of the agent/customer
                - orders_count: Number of orders
                - item_mean_price: Average price per item
                - order_mean_sum: Average order value
                - orders_total_sum: Total sales value
                
        Note:
            Returns top 150 agents by total sales value
        """
        df = self.df.get_prepocessdata_slice(period)
        report = df.groupby('agent_name')\
                    .agg({
                        'order_id': [('orders_count', 'count')],
                        'price': [('item_mean_price', 'mean')],
                        'sum': [('order_mean_sum', 'mean'), 
                               ('orders_total_sum', 'sum')]})\
                    .reset_index()
        
        report.columns = ['agent_name', 'orders_count', 'item_mean_price', 
                         'order_mean_sum', 'orders_total_sum']
        
        return report.sort_values('orders_total_sum', ascending=False)\
                    .head(150)\
                    .round(2)

    def get_item_type_report(self, period: TimeperiodType) -> pd.DataFrame:
        """
        Generate a report analyzing sales by product category.

        Args:
            period (TimeperiodType): Time period for the report ("day", "week", "month", "year")

        Returns:
            pd.DataFrame: Report containing the following columns:
                - item_type: Product category
                - orders_count: Number of orders
                - item_mean_price: Average price per item
                - order_mean_sum: Average order value
                - orders_total_sum: Total sales value
        """
        df = self.df.get_prepocessdata_slice(period)
        report = df.groupby('path_lvl_2')\
                    .agg({
                        'order_id': [('orders_count', 'count')],
                        'price': [('item_mean_price', 'mean')],
                        'sum': [('order_mean_sum', 'mean'), 
                               ('orders_total_sum', 'sum')]})\
                    .sort_values(('order_id','orders_count'), ascending=False)\
                    .reset_index()
        
        report.columns = ['item_type', 'orders_count', 'item_mean_price', 
                         'order_mean_sum', 'orders_total_sum']
        
        return report.round(2)

    def get_volumes_report(self, period: TimeperiodType) -> pd.DataFrame:
        """
        Generate a report analyzing sales by product volume.

        Args:
            period (TimeperiodType): Time period for the report ("day", "week", "month", "year")

        Returns:
            pd.DataFrame: Report containing the following columns:
                - volumes_ml: Product volume in milliliters
                - orders_count: Number of orders
                - item_mean_price: Average price per item
                - order_mean_sum: Average order value
                - orders_total_sum: Total sales value
        """
        df = self.df.get_prepocessdata_slice(period)
        report = df.groupby('volumes')\
                    .agg({
                        'order_id': [('orders_count', 'count')],
                        'price': [('item_mean_price', 'mean')],
                        'sum': [('order_mean_sum', 'mean'), 
                               ('orders_total_sum', 'sum')]})\
                    .sort_values(('order_id', 'orders_count'), ascending=False)\
                    .reset_index()
        
        report.columns = ['volumes_ml', 'orders_count', 'item_mean_price', 
                         'order_mean_sum', 'orders_total_sum']
        
        return report.round(2)

    def get_city_report(self, period: TimeperiodType) -> pd.DataFrame:
        """
        Generate a report analyzing sales by city.

        Args:
            period (TimeperiodType): Time period for the report ("day", "week", "month", "year")

        Returns:
            pd.DataFrame: Report containing the following columns:
                - city: City name
                - orders_count: Number of orders
                - item_mean_price: Average price per item
                - order_mean_sum: Average order value
                - orders_total_sum: Total sales value
                
        Note:
            Returns top 50 cities by order count
        """
        df = self.df.get_prepocessdata_slice(period)
        report = df.groupby('city')\
                    .agg({
                        'order_id': [('orders_count', 'count')],
                        'price': [('item_mean_price', 'mean')],
                        'sum': [('order_mean_sum', 'mean'), 
                               ('orders_total_sum', 'sum')]})\
                    .sort_values(('order_id','orders_count'), ascending=False)\
                    .reset_index()\
                    .head(50)
        
        report.columns = ['city', 'orders_count', 'item_mean_price', 
                         'order_mean_sum', 'orders_total_sum']
        
        return report.round(2)