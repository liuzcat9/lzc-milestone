from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

import bokeh
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import Legend

import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/res', methods=['POST', 'GET'])
def res():
    if request.method == 'POST':
        stock = request.form.getlist('stockname')
        result = request.form.getlist('check')

        # bokeh using API results
        r = requests.get('https://www.alphavantage.co/query?',
                         params={'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': stock[0],
                                 'apikey': os.getenv('ALPHA_API')})
        ex = r.json()
        df = pd.DataFrame.from_dict(ex["Time Series (Daily)"])
        df = df.T

        # convert data types in dataframe
        df.index = pd.to_datetime(df.index)
        df = df.apply(pd.to_numeric, axis = 1)

        # select data up to last year
        trunc_df = pd.DataFrame(df.loc["2020-06":"2019-06"])

        # add adjusted open price by calculating adjusted closing:closing price ratio
        trunc_df['8. adjusted open'] = trunc_df['5. adjusted close'] / trunc_df['4. close'] * trunc_df['1. open']

        p = figure(plot_width=600, plot_height=400, title="Ticker Lookup for " + stock[0], x_axis_label='Date', x_axis_type='datetime',
                   tools='pan, wheel_zoom, box_zoom, reset, save')

        # add a line renderer for each selected group
        colors = ["navy", "green", "firebrick", "black"]
        legend_list = []
        for i, result_type in enumerate(result):
            item = p.line(trunc_df.index, trunc_df[result_type], color=colors[i])
            legend_list.append((result_type[2:], [item]))

        legend = Legend(items=legend_list)
        p.add_layout(legend, 'right')

        plot_script, plot_div = components(p)

        return render_template("res.html", stockname=stock[0], bscript=plot_script, bdiv=plot_div)
