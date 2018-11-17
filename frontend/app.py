from flask import Flask,render_template
from welly import Well
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!' 

@app.route('/about')
def about():
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


