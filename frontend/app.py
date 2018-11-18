from flask import Flask,render_template,jsonify
from welly import Well
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!' 

@app.route('/get-plot')
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

@app.route('/GeologicalFormation')
def GFormation():
    return render_template('geological-formation.html')
    
@app.route('/plot')
def plot():
    p = Well.from_las('static/las-files/6307_d.las')
    p.plot()
    plt.savefig('static/images.png')
    return render_template('base.html',name = 'plot', url='static/images.png')
    
if __name__ == '__main__':
    app.run()


