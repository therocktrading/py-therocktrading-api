from TheRockTrading import Client
import pandas as pd
import datetime
import os


#PARAMS
period = 60 #every hour
symbol = 'BTCEUR'
start_date = '2022-02-01T00:00:00Z' #format y-m-dThh:mm:ssZ


class Downloader:
    def __init__(self):
        self.client = Client()

    def query(self, period, symbol, start_date):
        self.period = period
        self.symbol = symbol
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        self.now = datetime.datetime.now() - datetime.timedelta(days=1)
        self.df = pd.DataFrame()
        
    def ohcl(self):
        df = pd.DataFrame(self.client.ohlc_statistics(self.symbol, 
                                                        period=self.period, 
                                                        before=self.start_date, 
                                                        order='ASC'))
        return df

    def download(self):
        while self.start_date < self.now:
            self.df = self.df.append(self.ohcl())
            self.start_date += datetime.timedelta(days=1)
        self.postprocess()
        self.save()
        
    def postprocess(self):
        self.df.drop_duplicates(subset=['interval_starts_at'], 
                                inplace=True)
        self.df.sort_values(by=['interval_starts_at'], 
                            inplace=True)

    def save(self):
        file_path = f"data/history_{self.symbol}.csv"
        if not os.path.exists(file_path):
            os.makedirs(file_path.split("/")[0], exist_ok=True)
        self.df.to_csv(file_path, index=False)


if __name__=='__main__':
    #DOWNLOAD CLASS
    downloader = Downloader()    
    downloader.query(period, symbol, start_date)
    downloader.download()