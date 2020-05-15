from flask import Flask, render_template, request, redirect

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
      result = request.form.getlist('check')
      print(type(result))
      return render_template("res.html", result = result)

if __name__ == '__main__':
  app.run(port=33507)
