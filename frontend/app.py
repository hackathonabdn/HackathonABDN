from flask import Flask,render_template,jsonify
from welly import Well
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def home():
    return 'Geological Formation' 

@app.route('/get-plot', methods=['POST', 'OPTIONS', 'GET'])
def getplots():
    p = Well.from_las('static/las-files/6307_d.las')
    gr = p.data['GR']
    gr[np.isnan(gr)] = 0
    payload = {'curve': list(gr),
               'depth': list(gr.basis)}
    return jsonify(payload)

@app.route('/about/<x>/<y>')
def about(x,y):
    return render_template('about.html')

@app.route('/gasoil')
def gasoil():
    return render_template('gasoil.html')

@app.route('/Gformation')
def Gformation():
    return render_template('Gformation.html')
    
@app.route('/plot')
def plot():
    p = Well.from_las('static/las-files/6307_d.las')
    p.plot()
    plt.savefig('static/images.png')
    return render_template('base.html',name = 'plot', url='static/images.png')
    
@app.route('/getplotdata/<wellname>', methods=['POST', 'OPTIONS', 'GET'])
def getplotdata(wellname):
    p = Well.from_las('static/las-files/'+wellname+'.las')
    gr = p.data['GR']
    gr [np.isnan(gr)] = 0
    payload = {'curve': list(gr),
    'depth': list(gr.basis)}
    return jsonify(payload)  

@app.route('/retrieve/<wellname>/<fr>/<to>', methods=['POST', 'OPTIONS', 'GET'])
def retrieve(wellname,fr,to):
    p = Well.from_las('static/las-files/'+wellname+'.las')
    gr = p.data['GR']
    gr [np.isnan(gr)] = 0
    payload = {'curve': list(gr),
    'depth': list(gr.basis)}
    return jsonify(payload)
        
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run()


