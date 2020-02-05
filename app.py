#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Shoaib
"""

from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
import numpy as np
from tensorflow.keras.models import load_model

def return_prediction(model,json):
    
    content = list(map(float, [json[col] for col in cols] ))
    
    array = np.reshape(content,(1,-1))
    result = model.predict(array)
    
    #if result[0][0]<0.036:
    #    return False
    #else:
    #    return True
    
    return result[0][0]

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

sepsis_model = load_model('model.h5')

cols=['HR',  'O2Sat',  'Temp',  'SBP',  'MAP',  'DBP',  'Resp',  'EtCO2',
       'BaseExcess' ,  'HCO3' ,  'FiO2' ,  'pH' ,  'PaCO2' ,  'SaO2' ,  'AST' ,  'BUN',
       'Alkalinephos' ,  'Calcium' ,  'Chloride' ,  'Creatinine' ,  'Bilirubin_direct' ,
       'Glucose' ,  'Lactate',  'Magnesium' ,  'Phosphate' ,  'Potassium' ,
       'Bilirubin_total' ,  'TroponinI' ,  'Hct' ,  'Hgb' ,  'PTT' ,  'WBC' ,
       'Fibrinogen' ,  'Platelets' ,  'Age' ,  'Gender' ,  'Unit1' ,  'Unit2' ,
       'HospAdmTime' ,  'ICULOS' ]
 

@app.route('/')
@cross_origin()
def server_status():
    
    return jsonify({ "status" : "online" })

@app.route('/prediction', methods=['POST'] )
@cross_origin()
def prediction():
    
    body = request.get_json()
    
    result = return_prediction(sepsis_model,body)
    
    return jsonify({ "prediction" : str(result) })

if __name__ == '__main__':
    app.run(debug=True)