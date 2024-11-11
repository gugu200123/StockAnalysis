import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(stocks, start, end):
    data = yf.download(stocks, start=start, end=end)
    data = data[['Adj Close', 'Volume']]
    data.fillna(method='ffill', inplace=True)
    return data

def plot_adjusted_prices(data, stocks):
    plt.figure(figsize=(14, 7))
    for stock in stocks:
        data['Adj Close'][stock].plot(label=stock)
    plt.xlabel('Date')
    plt.ylabel('Adjusted Price')
    plt.legend()
    plt.show()

def plot_trading_volume(data, stocks):
    plt.figure(figsize=(14, 7))
    for stock in stocks:
        data['Volume'][stock].plot(label=stock)
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.show()

def plot_correlation(data):
    correlation = data['Adj Close'].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.show()

def plot_moving_averages(data, stocks):
    for stock in stocks:
        data['SMA20_' + stock] = data['Adj Close'][stock].rolling(window=20).mean()
        data['SMA50_' + stock] = data['Adj Close'][stock].rolling(window=50).mean()

    plt.figure(figsize=(14, 7))
    for stock in stocks:
        data['Adj Close'][stock].plot(label=stock + ' Adjusted Price')
        data['SMA20_' + stock].plot(label=stock + ' SMA 20')
        data['SMA50_' + stock].plot(label=stock + ' SMA 50')
    plt.xlabel('Date')
    plt.ylabel('Adjusted Price')
    plt.legend()
    plt.show()

def plot_buy_sell_signals(data, stocks):
    for stock in stocks:
        data['Signal_' + stock] = 0
        data['Signal_' + stock] = data['SMA20_' + stock] > data['SMA50_' + stock]

        plt.figure(figsize=(14, 7))
        plt.plot(data['Adj Close'][stock], label=stock + ' Adjusted Price')
        plt.plot(data['SMA20_' + stock], label=stock + ' SMA 20')
        plt.plot(data['SMA50_' + stock], label=stock + ' SMA 50')
        plt.scatter(data.index, data['Adj Close'][stock], c=data['Signal_' + stock], cmap='viridis', label='Buy/Sell Signal')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Price')
        plt.legend()
        plt.show()

stocks = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA',  'ABEV3.SA',  'MGLU3.SA',  'WEGE3.SA']
start = "2023-01-01"
end = "2024-01-01"
data = load_data(stocks, start, end)

print(data.head())
plot_adjusted_prices(data, stocks)
plot_trading_volume(data, stocks)
plot_correlation(data)
plot_moving_averages(data, stocks)
plot_buy_sell_signals(data, stocks)
