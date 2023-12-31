import os
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns

class Data:
    def __init__(self):
        self.directory = 'C:/Users/cindy/OneDrive/Documents/Python Projects/Input and Automated Reporting Tool/data'
        self.filename = 'may2023_FTA_VRM.csv'
        self.file_path = os.path.join(self.directory, self.filename)
        self.agency_options = ["Massachusetts Bay Transportation Authority","Long Beach Transit","Los Angeles County Metropolitan Transportation Authority "]

    def get_data(self):
        df = pd.read_csv(self.file_path)
        df = df.loc[df['Agency'].isin(self.agency_options)]
        return df
    
    def agency_list(self, df):
        agency_list = df['Agency'].unique().tolist()
        return agency_list

    def mode_list(self, df, agency:str):
        mode_list = df.loc[df['Agency'] == agency]['Mode'].unique().tolist()
        return mode_list
    
    def forecast(self, df, agency:str, mode:str):
        data = df.loc[(df['Agency'] == agency)&(df['Mode']==mode)]
        data['Date'] = pd.to_datetime(data['Date'], format='%m/%Y')
        df2 = data[['Date','Total']].copy().reset_index(drop=True)
        df2.columns = ['ds', 'y']
        m = Prophet(interval_width=0.95, daily_seasonality=True)
        model = m.fit(df2)
        future = m.make_future_dataframe(periods=12,freq='M')
        forecast = m.predict(future)
        plot1 = m.plot(forecast)

        ax = plot1.gca()
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.lineplot(forecast.loc[forecast['ds'] > '2023-05-31'], x='ds', y='yhat', ax=ax2, label='Forecast')
        ax2.legend()

        return plot1, fig2