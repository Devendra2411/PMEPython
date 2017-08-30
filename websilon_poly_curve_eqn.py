# -*- coding: utf-8 -*-
"""
Module to find the polynomial curve equation to the  model of certain data points with a order of n

Created on Tue Aug  8 16:28:14 2017
@author: 502694234
"""
# Generic import
import os
import json
# Package import
from flask import request
from flask import Flask
from flask import jsonify
from flask_cors import cross_origin
import numpy as np

app = Flask(__name__)
# Configuring the port
port = int(os.getenv("PORT", 3001))

@app.route('/coefficients', methods = ['POST'])
@cross_origin()
def find_poly_curve_eqn():
    poly_constants = {}
    x_points = []
    y_points = []
    y_result = []
    constant_list_new = []
    if request.headers['Content-Type'] == 'application/json':
        coordinates = json.loads(request.data.decode(encoding='UTF-8'))
        # type casting the x and y data points from String to float
        for each_x_point in coordinates['x']:
            x_points.append(float(each_x_point))
        for each_y_point in coordinates['y']:
            y_points.append(float(each_y_point))
        # X - coordinates of the Model data points
        x_input = np.array(x_points)
        # Y - coordinates of the Model data points
        y_inputs = np.array(y_points)
        # Order of the curve
        order = int(coordinates['orderOfFit'])
        # finding the polynomial curve equation
        constants = np.polyfit(x_input, y_inputs, order)
        constants_list = constants.tolist()
        for each in constants_list:
          value = round(each, 5)
          constant_list_new.append(value)
        points_finder = np.poly1d(constants)
        # Finding the Exact values of polynomial curve equation
        for each_point in x_points:
            y_result.append(points_finder(each_point))
        # Adding the results to the dictionary
        poly_constants['coefficient'] = constant_list_new
        poly_constants['y_result'] = y_result
        poly_constants['x_input'] = x_points
        poly_constants['y_input'] = y_points
        poly_constants['status'] = 'SUCCESS'
    else:
        poly_constants['status'] = 'FAILURE'
    return jsonify(poly_constants)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)


