from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

import bokeh
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components

import config

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/res',methods = ['POST', 'GET'])
def res():
   if request.method == 'POST':
      stock = request.form.getlist('stockname')
      result = request.form.getlist('check')

      # bokeh using API results
      r = requests.get('https://www.alphavantage.co/query?',
                       params={'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': stock, 'apikey': config.key})
      ex = r.json()
      df = pd.DataFrame.from_dict(ex["Time Series (Daily)"])
      df = df.T

      # convert data types in dataframe
      df.index = pd.to_datetime(df.index)
      df = df.apply(pd.to_numeric, axis=1)

      df_src = ColumnDataSource(df)

      p = figure(plot_width=400, plot_height=400, x_axis_type='datetime', tools='pan,wheel_zoom,box_select,reset')

      # add a line renderer for each selected group
      colors = ["navy", "green", "firebrick", "grey"]
      for i, result_type in enumerate(result):
          p.line(df.index, df[result_type], color = colors[i], legend_label = result_type[2:])

      plot_script, plot_div = components(p)

      return render_template("res.html", result = result, bscript = plot_script, bdiv = plot_div)

if __name__ == '__main__':
  app.run(port=33507)
