#function to plot the data

import matplotlib.pyplot as plt 

def plot_graph(data, filename):
    plt.figure(figsize=(12.5, 4.5))
    plt.plot(data[-300:].close,label='Close Price',color='blue')
    plt.plot(data[-300:].dcl,color='black',linestyle='--',alpha=0.3)
    plt.plot(data[-300:].dcm,color='orange',label='DCM')
    plt.plot(data[-300:].dcu,color='black',linestyle='--',alpha=0.3,label='DCL,DCU')
    plt.legend()
    plt.title('AAPL stock price with Donchian Channels')
    plt.xlabel('Date')
    plt.ylabel('Close')
    plt.savefig(filename)