from TheRockTrading import Client
import plotly.graph_objs as go
from datetime import datetime
import multiprocessing.dummy
import pandas as pd
import os

dir = "data/"

def asks_bids(pair: str) -> dict:
    orderbook = client.orderbook(pair)
    bids = orderbook["bids"] if len (orderbook["bids"]) > 0 else None
    asks = orderbook["asks"] if len (orderbook["asks"]) > 0 else None
    return asks, bids
    
def save(df: pd.DataFrame) -> None:
    path = dir + "orderbook.csv"
    if not os.path.exists(path):
        os.makedirs(dir, exist_ok=True)
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, index=False, header=False, mode="a")
    
def unpack(pair: str, date: datetime, book_tag: str, book: dict) -> dict:
    pairs, dates, book_tags, prices, amounts = [], [], [], [], []
    for idx in range(len(book)):
        pairs.append(pair)
        dates.append(date)
        book_tags.append(book_tag)
        prices.append(book[idx]['price'])
        amounts.append(book[idx]['amount'])
    return {
        "pairs": pairs, 
        "datetime": dates, 
        "orderbook": book_tags, 
        "price": prices, 
        "amounts": amounts
    }
    
def plot(df):
    bid_plot = {
    "mode": "lines+markers", 
    "name": "bid", 
    "type": "scatter", 
    "x": df.price[df.orderbook == "bid"],
    "y": df.amounts[df.orderbook == "bid"]
    }
    ask_plot = {
    "mode": "lines+markers", 
    "name": "ask", 
    "type": "scatter", 
    "x": df.price[df.orderbook == "ask"],
    "y": df.amounts[df.orderbook == "ask"]
    }
    layout = {
    "title": "Limited Order Book", 
    "xaxis": {"title": "price"}, 
    "yaxis": {"title": "amount"}
    }
    fig = go.Figure(data=([bid_plot, ask_plot]), layout=layout)
    path = dir + f"orderbook_{df.pairs.values[0]}.html"
    fig.write_html(path)
        
def generate_df(pair: str) -> None:
    asks, bids = asks_bids(pair)
    date = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    
    df_asks = pd.DataFrame(
        unpack(
            pair = pair,
            date = date, 
            book_tag = "ask",
            book = asks            
        )
    )
    df_bids = pd.DataFrame(
        unpack(
            pair = pair,
            date = date, 
            book_tag = "bid",
            book = bids            
        )
    )
    df = pd.concat([df_asks, df_bids])
    save(df)
    plot(df)

def main(pairs: list) -> None:
    pool = multiprocessing.dummy.Pool(8)
    pool.map(generate_df, pairs) 
    pool.close()
    pool.join()


if __name__ == "__main__":
    global client
    client = Client(API="", API_SECRET="", staging=False)
    pairs = [fund['id'] for fund in client.funds()['funds']]
    main(pairs)
