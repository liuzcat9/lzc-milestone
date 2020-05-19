from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import numpy as np

import bokeh
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components

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

      # dummy bokeh
      r = requests.get('https://www.alphavantage.co/query?',
                       params={'function': 'TIME_SERIES_DAILY', 'symbol': stock, 'apikey': 'demo'})
      ex = r.json()
      df = pd.DataFrame.from_dict(ex["Time Series (Daily)"])
      df = df.T

      df_src = ColumnDataSource(data=dict(
          x=pd.to_datetime(df.index),
          y=pd.to_numeric(df['4. close'])))

      p = figure(plot_width=400, plot_height=400, x_axis_type='datetime', tools='pan,wheel_zoom,box_select,reset')
      # add a line renderer

      p.line('x', 'y', source=df_src)
      plot_script, plot_div = components(p)

      return render_template("res.html", result = result, bscript = plot_script, bdiv = plot_div)

if __name__ == '__main__':
  app.run(port=33507)
