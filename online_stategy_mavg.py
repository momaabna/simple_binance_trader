#!/bin/python3
import numpy as np
from binance import Client
from config import *
import time,datetime
import os

#////Init///
#//Parameters
n=60
folder ='datamo/'
pair ="LUNAUSDT"
#g =get_data(folder)
data =[0,100]
nb =10
ns =5
client = Client(api_key, api_secret)
print('[!] Start and Waiting For bot to collect Data ...')
with open('logs.txt','a') as f:
    f.write('[!] Start and Waiting For bot to collect Data ...\n')
#/////////////Getting online Data Generator////////////
def get_online_data(s,t):
    time.sleep((60-datetime.datetime.now().minute)*60-datetime.datetime.now().second)
    
    while True:
        btc_price = client.get_symbol_ticker(symbol=s)
        yield [btc_price['symbol'],float(btc_price['price'])]
        with open('logs.txt','a') as f:
            f.write('[+] Get Price from binance '+str([btc_price['symbol'],float(btc_price['price'])])+' \n')
        time.sleep(t)




#////////////Old data generator///////////////

def get_data(folder):
    files = os.listdir(folder)
    files.sort()
    c =0
    for file in files:
        fn = folder+file
        arr = np.loadtxt(fn,delimiter=',')
        for t,p,*_ in arr:
            c+=1
            if c%(60)==0:
                yield [t,p]

#//buy and sell simulation
def buy(data,p,c):
    cc =p*c
    data[0] =data[0]+c
    data[1] =data[1]-cc -0.00075*cc
    return data

def sel(data,p,c):
    cc =p*c
    data[0] =data[0]-c -0.00075*c
    data[1] =data[1]+cc
    return data 
#///////////Buy and Sell Online///////////////////
"""
def buy(data,p,c):
    order = client.create_order(symbol=pair,side='BUY',type='MARKET',quantity=c)
    p =float(order['fills'][0]['price'])
    com=float(order['fills'][0]['commission'])
    c=float(order['fills'][0]['qty'])
    cc =p*(c)
    data[0] =data[0]+c#-com
    data[1] =data[1]-cc
    print(order)
    return data

def sel(data,p,c):
    order = client.create_order(symbol=pair,side='SELL',type='MARKET',quantity=c)
    p =float(order['fills'][0]['price'])
    com=float(order['fills'][0]['commission'])
    c=float(order['fills'][0]['qty'])
    cc =p*(c)
    data[0] =data[0]-c
    data[1] =data[1]+cc#-com
    print(order)
    return data
"""

#//////Strategy MVAVG/////////////////////////////
def avg(n,prices):
    s=0
    for i in range(-1,-n-1,-1):
        s+=prices[i]
    return s/n
def mavg_strategy(data, g, nb,ns,history):
    prices =[]
    avb = []
    avs =[]
    for i in range(-nb,-1,1):
        prices.append(float(history[i][4]))
    while True:
        with open('flag.txt','r') as f:
                if int(f.read())==0:
                    print('[-] Terminated by user')
                    quit()
        try:
            t,p = next(g)
            prices.append(p)
        except:
            return data[0]*p+data[1]
        if len(prices) >nb:
            avb.append(avg(nb,prices))
            avs.append(avg(ns,prices))
            diff = np.array(avs) -np.array(avb)
            if len(diff)>2:
                if diff[-1] >0 and diff[-2]<=0  and (avb[-1]>avb[-2]) :
                    buy(data, p, data[1]/(p +0.1*p))
                    print('Buy at :',p,data)
                    with open('logs.txt','a') as f:
                        f.write('Buy at :'+str(p)+str(data)+' \n')
                    while True:
                        with open('flag.txt','r') as f:
                            if int(f.read())==0:
                                data = sel(data,p[2],q)
                                print('Sel at :',p,data)
                                print('[-]  Selled and Terminated by user')
                                quit()
                        try:
                            t,p = next(g)
                            prices.append(p)
                        except:
                            return data[0]*p+data[1]
                        avb.append(avg(nb,prices))
                        avs.append(avg(ns,prices))
                        diff = np.array(avs) -np.array(avb)
                        if diff[-1]<0 and diff[-2]>=0 and (avb[-1]<avb[-2]):
                            sel(data, p, data[0]-0.00075*data[0])
                            print('Sel at :',p,data)
                            with open('logs.txt','a') as f:
                                f.write('Sel at :'+str(p)+str(data)+' \n')
                            break
                        del avb[0],avs[0],prices[0]
                del avb[0],avs[0],prices[0]


if __name__=='__main__':
    g = get_online_data(pair, 3600)
    history = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, "1 day ago")
    d=mavg_strategy(data, g, nb, ns,history)
