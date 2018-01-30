import pandas as pd

from flask import render_template
from flask import Response
from flask_restful import Resource
from flask_restful import reqparse

from ml_model.model import get_feature_importances_fig
from resources.utils import pandas_plot_to_html
import logging

import redis


cache = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)


class SubmitJewelryForm(Resource):
    """Resource class to handle the a post or get request.

    The input fields defined in the html form are loaded into the class
    instance via the flask_restful.reqparse.RequestParser.

    """

    def __init__(self, model, features, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('probe', type=float)
        self.parser.add_argument('weight', type=float)
        self.parser.add_argument('jew_type', type=float)
        self.parser.add_argument('jew_weight', type=float)
        self.parser.add_argument('complexity', type=int)
        self.parser.add_argument('return_html', type=bool, default=False)
        args = self.parser.parse_args()
        self.return_html = args['return_html']
        self.user_inputs = {k: v
                            for k, v in args.items()
                            if v is not None and k is not 'return_html'}
        self.model = model
        self.features = features
        super().__init__()


    def get(self):
        """
            get request
        """
        prev_search = cache.lrange('last10keys', 0, 4)
        search_array = [[i for i in line.split(' ')] for line in prev_search]
        
        print(f'search_array {search_array}')
        res = Response(
            render_template('eval_result.html',
                            left_panel='evaluation_form.html',
                            tab_0='dataframe.html',
                            tab_1='plot.html',
                            right_panel='right_panel.html',
                            search_array=search_array)
        )
        return res


    def post(self):
        """
            post request.
        """
        # make a price prediction
        prediction = self.predict()
        
        fig = get_feature_importances_fig(self.model, self.features, prediction)
        img = pandas_plot_to_html(fig)

        # reduce redis list 
        cache.ltrim('last10keys',0, 4)
        
        combined_cache = list(self.user_inputs.values())
        combined_cache.append(prediction)
        cache.lpush('last10keys',  ' '.join(map(str, combined_cache)))
        
        prev_search = cache.lrange('last10keys', 0, 4)
                
        #search_array = [[i for i in map(float, line.split(' '))] for line in prev_search]
        search_array = [[i for i in line.split(' ')] for line in prev_search]
        
        #logging.info(f'search_array {search_array}')
        
        
        
        # different response depending if coming from UI or from
        # a post request command
        if self.return_html:
            res = Response(
                render_template("eval_result.html",
                                left_panel='evaluation_form.html',
                                right_panel='right_panel.html',
                                tab_0='prediction.html',
                                tab_1='plot.html',
                                prediction_label='price',
                                prediction=prediction,
                                plot_title="Features %price importance with GradientBoost",
                                search_array=search_array,
                                plot=img,
                                **self.user_inputs),
                status=200)
        else:
            res = prediction
        return res


    def predict(self):
        """Make prediction using the pretrained model.

        Returns:
            The single prediction based on inputs
        """
        pred_data = pd.DataFrame(self.user_inputs, index=[0])
        prediction = self.model.predict(pred_data)
        return round(prediction[0], 2)

