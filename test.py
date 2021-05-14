from pandas.core.indexing import is_nested_tuple
import pygsheets
import pandas as pd
import yfinance as yf

tickers = [
    ['BTC',0.16982501],
    ['ETH',3.5225338],
    ['ADA',2036.9292],
    ['LTC',1.012478]
    #['SHIB',3233305.43],
    #['GRT',271.97709258]
]

frames = []

for ticker in tickers:
    df = yf.download(tickers=ticker[0]+'-GBP', period='ytd', interval='1d')
    df.sort_index(ascending=False, inplace=True)
    df.reset_index(inplace=True)
    df['Ticker'] = ticker[0]
    df['Owned'] = ticker[1]
    frames.append(df)
    
df = pd.concat(frames)
df = pd.melt(df, id_vars=['Date','Ticker','Owned'])
df = df.rename(columns={'variable':'Metric','value':'Value'})

#authorization
gc = pygsheets.authorize(service_file='/Users/mdunford/crypto_price_data/creds.json')

#open the google spreadsheet
sh = gc.open('Crypto balance')

#select the first sheet 
crypto_data = sh[1]

#update the first sheet with df, starting at cell B2. 
crypto_data.set_dataframe(df,(1,1))
