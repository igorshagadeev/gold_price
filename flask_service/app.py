# change default plotting backend for the complete application
import matplotlib
matplotlib.use('agg')

from flask import Flask
from flask import render_template

from flask_restful import Api

from ml_model.model import get_model
from resources.submit_form import SubmitJewelryForm


app = Flask(__name__)
api = Api(app)


#@app.route('/info')
#def info():
    #name = 'user'
    #visits = 3
    #html = "<h3>Hello {name}!</h3>" \
           #"<b>Visits:</b> {visits}"
    #return html


#@app.route('/')
#def index():
    #return render_template('index.html')



## get data from model application
model, features = get_model()


api.add_resource(
    SubmitJewelryForm, '/',
    resource_class_kwargs={
        'model': model,
        'features': features,})
    

















