import pandas as pd
import yfinance as yf
from .BasicFunction import CheckPath 


def StockDataDownload(_stock_id, _start, _end, savepath):
    if CheckPath(savepath):        
        data = yf.download(_stock_id, start = _start, end = _end)
        print(f"Finish downloaded")
        data.drop(['Adj Close'], axis=1, inplace=True)
        data.columns = ["open","high","low","close","volume"]
        # download Stock-data from yahoo
        # and drop 1 column, "Adj Close" which are no needs to use 
        data.to_json(f"{savepath}/stockdata.json", orient='records')
        print(f"Saving {_stock_id} stock data file at {savepath} \r\n")
        # Save the data as .json Type
        # data name save as {Stock_Id}+{Star_day}+{End_day}.json
        data = pd.concat([pd.DataFrame(data.index).reset_index(drop=True), data.reset_index(drop=True)], axis=1)
        data.to_json(f"{savepath}/origin_stockdata.json", orient='records')
        # Save another data but with "Date"
    else:
        print("No folder to storge data\r\n")
