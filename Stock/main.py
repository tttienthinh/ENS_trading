#!/usr/bin/env python
# coding: utf-8

# In[2]:


# IMPORTS
import pandas as pd
import os
import time
from binance.client import Client

from datetime import datetime, timedelta

from ta import add_all_ta_features
from ta.utils import dropna

import webbrowser
from IPython.display import HTML, clear_output


# In[9]:


### API
api_key = 'BINANCE API'
api_secret = 'BINANCE SECRET KEY'


# In[10]:


client = Client(api_key, api_secret)

datas = ['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'volume_adi', 'volume_obv', 'volume_cmf', 'volume_fi', 'volume_mfi', 'volume_em', 'volume_sma_em', 'volume_vpt', 'volume_nvi', 'volume_vwap', 'volatility_atr', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'volatility_bbw', 'volatility_bbp', 'volatility_bbhi', 'volatility_bbli', 'volatility_kcc', 'volatility_kch', 'volatility_kcl', 'volatility_kcw', 'volatility_kcp', 'volatility_kchi', 'volatility_kcli', 'volatility_dcl', 'volatility_dch', 'volatility_dcm', 'volatility_dcw', 'volatility_dcp', 'volatility_ui', 'trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'trend_sma_fast', 'trend_sma_slow', 'trend_ema_fast', 'trend_ema_slow', 'trend_adx', 'trend_adx_pos', 'trend_adx_neg', 'trend_vortex_ind_pos', 'trend_vortex_ind_neg', 'trend_vortex_ind_diff', 'trend_trix', 'trend_mass_index', 'trend_cci', 'trend_dpo', 'trend_kst', 'trend_kst_sig', 'trend_kst_diff', 'trend_ichimoku_conv', 'trend_ichimoku_base', 'trend_ichimoku_a', 'trend_ichimoku_b', 'trend_visual_ichimoku_a', 'trend_visual_ichimoku_b', 'trend_aroon_up', 'trend_aroon_down', 'trend_aroon_ind', 'trend_psar_up', 'trend_psar_down', 'trend_psar_up_indicator', 'trend_psar_down_indicator', 'trend_stc', 'momentum_rsi', 'momentum_stoch_rsi', 'momentum_stoch_rsi_k', 'momentum_stoch_rsi_d', 'momentum_tsi', 'momentum_uo', 'momentum_stoch', 'momentum_stoch_signal', 'momentum_wr', 'momentum_ao', 'momentum_kama', 'momentum_roc', 'momentum_ppo', 'momentum_ppo_signal', 'momentum_ppo_hist', 'others_dr', 'others_dlr', 'others_cr']
drop  = ['Open', 'High', 'Low', 'Volume', 'volume_adi', 'volume_obv', 'volume_cmf', 'volume_fi', 'volume_mfi', 'volume_em', 'volume_sma_em', 'volume_vpt', 'volume_nvi', 'volume_vwap', 'volatility_atr', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'volatility_bbw', 'volatility_bbp', 'volatility_bbhi', 'volatility_bbli', 'volatility_kcc', 'volatility_kch', 'volatility_kcl', 'volatility_kcw', 'volatility_kcp', 'volatility_kchi', 'volatility_kcli', 'volatility_dcl', 'volatility_dch', 'volatility_dcm', 'volatility_dcw', 'volatility_dcp', 'volatility_ui', 'trend_macd', 'trend_macd_signal', 'trend_macd_diff', 'trend_sma_fast', 'trend_sma_slow', 'trend_ema_fast', 'trend_ema_slow', 'trend_adx_pos', 'trend_adx_neg', 'trend_vortex_ind_pos', 'trend_vortex_ind_neg', 'trend_vortex_ind_diff', 'trend_trix', 'trend_mass_index', 'trend_cci', 'trend_dpo', 'trend_kst', 'trend_kst_sig', 'trend_kst_diff', 'trend_ichimoku_conv', 'trend_ichimoku_base', 'trend_ichimoku_a', 'trend_ichimoku_b', 'trend_visual_ichimoku_a', 'trend_visual_ichimoku_b', 'trend_aroon_up', 'trend_aroon_down', 'trend_aroon_ind', 'trend_psar_up', 'trend_psar_down', 'trend_psar_up_indicator', 'trend_psar_down_indicator', 'trend_stc', 'momentum_stoch_rsi', 'momentum_stoch_rsi_k', 'momentum_stoch_rsi_d', 'momentum_tsi', 'momentum_uo', 'momentum_stoch', 'momentum_stoch_signal', 'momentum_wr', 'momentum_ao', 'momentum_kama', 'momentum_roc', 'momentum_ppo', 'momentum_ppo_signal', 'momentum_ppo_hist', 'others_dr', 'others_dlr', 'others_cr']


# In[11]:


def df_window(df, name, opening=False):
    with open(f"{name}.html", "w+") as f:
        f.write(df.render())
        if opening:
            webbrowser.open(f.name)
        f.close()


def get_data(symbol="BTCUSDT", time=45, delta="1m"):
    timestamp = int((datetime.timestamp(datetime.now() - timedelta(minutes=time))) * 1_000)
    bars = client.get_historical_klines(symbol, delta, timestamp, limit=100)
    df = pd.DataFrame(bars, columns =['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volume', 
                                  'CloseTime', '1', '2', '3', '4', '5']) 

    df = df.drop(['CloseTime', '1', '2', '3', '4', '5'], axis=1)
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"]//1_000,unit='s')
    for convert in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[convert] = df[convert].astype(float)
    return df

def get_custom(df):
    # MACD calcul la moyenne mobile de la dérivé de trend_macd_diff
    df["MACD_deriv"] = df.trend_macd_diff.diff(periods=1).rolling(4, min_periods=1).mean()
    
    # SMA calcul la moyenne mobile de la dérivé de trend_macd_diff
    sma_diff = df["trend_sma_fast"]-df["trend_sma_slow"]
    df["SMA_deriv"] = (sma_diff/sma_diff.mean()).diff(periods=1).rolling(4, min_periods=1).mean()
    
    # EMA calcul la moyenne mobile de la dérivé de trend_macd_diff
    ema_diff = df["trend_ema_fast"]-df["trend_ema_slow"]
    df["EMA_deriv"] = (ema_diff/ema_diff.mean()).diff(periods=1).rolling(4, min_periods=1).mean()

    return df

def get_style(df):
    df = df.drop(drop, axis=1)
    df = df.rename(columns={"Close": "Price"})
    
    # RSI traitement
    df = df.rename(columns={"momentum_rsi": "RSI"})
    
    # MACD traitement
    df = df.rename(columns={"MACD_deriv": "MACD"})
    
    # SMA traitement
    df = df.rename(columns={"SMA_deriv": "SMA"})
    
    # EMA traitement
    df = df.rename(columns={"EMA_deriv": "EMA"})
    
    
    # ADX traitement
    df = df.rename(columns={'trend_adx': "ADX"})
    
    # Reorganise
    df = df[["TimeStamp", "Price", "RSI", "MACD", "SMA", "EMA", "ADX"]]
    
    html = (df
        .style
        .set_table_styles([dict(selector="tr:hover", 
                                props=[("background-color", "#ffff99")])]) # Hover
        .background_gradient(subset='RSI', cmap='RdYlGn_r', vmin=20., vmax=80.) # RSI
        .background_gradient(subset='MACD', cmap='RdYlGn', vmin=-3, vmax=3) # MACD
        .background_gradient(subset='MACD', cmap='RdYlGn', vmin=-3, vmax=3) # MACD
        .background_gradient(subset='SMA', cmap='RdYlGn', vmin=-0.5, vmax=0.5) # SMA
        .background_gradient(subset='EMA', cmap='RdYlGn', vmin=-0.5, vmax=0.5) # SMA
            
        .background_gradient(subset='ADX', cmap='binary', vmin=20., vmax=80.) # ADX

        .highlight_null('red')
        .set_caption("Vert : Achat - Rouge : Vente *** Noir : fiable - Blanc : à Eviter")
           )
    
    return html


# In[ ]:


cryptos = ['BTC', 'ETH', 'BCH', 'XRP', 
           'DASH', 'LTC', 'ETC', 'ADA', 
           'IOTA', 'XLM', 'EOS', 'NEO', 
           'TRX', 'ZEC', 'BNB', 'XTZ'
          ]

while True:
    print("**********************************************************************")
    cryptos_df = []
    crypto_df = pd.DataFrame(columns=datas)
    for crypto in cryptos[:]:
        print(crypto)
        df = get_data(f"{crypto}USDT", 45)
        df_ = add_all_ta_features(df, 
              open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True
        )
        df_ = get_custom(df_)
        cryptos_df.append(df_)
        last_row = df_.iloc[[-1]]
        last_row.insert(0, "Name", crypto) 
        crypto_df = crypto_df.append(last_row)
    crypto_df = crypto_df.set_index('Name')
    
    html = get_style(crypto_df)
    df_window(html, "main", True)
    os.system('spd-say "Ready to Analyse"')
    for i in range(len(cryptos)):
        html = get_style(cryptos_df[i])
        df_window(html, f"Details/{cryptos[i]}")
    time.sleep(61 - datetime.now().second)
    clear_output()

