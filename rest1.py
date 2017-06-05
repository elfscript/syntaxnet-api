# -*- coding: utf-8 -*-

"""
Copyright 2016-2017 Thomas Pellissier Tanon All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

from flask import Flask, request, jsonify, redirect
from flask_swaggerui import build_static_blueprint, render_swaggerui
from syntaxnet_wrapper import parser, language_code_to_model_name
from werkzeug.exceptions import BadRequest, InternalServerError

# Overrides available languages map
language_code_to_model_name['en'] = 'English'  # Do not use Parsey McParseface

# Flask setup
app = Flask(__name__, static_url_path='/mystatic')
logging.basicConfig(level=logging.INFO)
print(app.static_url_path)
print(app.static_folder)

from flask import url_for

#xxx print(url_maps)
def list_routes(): 
  import urllib 
  output = [] 
  for rule in app.url_map.iter_rules(): 
    options = {} 
    for arg in rule.arguments: 
      options[arg] = "[{0}]".format(arg) 
      methods = ','.join(rule.methods) 
      url = url_for(rule.endpoint, **options) 
      line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url)) 
      output.append(line)     
   
  for line in sorted(output): 
    print line




@app.route('/')
def _root():
    return "I am a pig" #redirect('/v1')

from flask.ext.cors import CORS, cross_origin

@app.route('/v1')
def _v1():
    return render_swaggerui(swagger_spec_path='/v1/swagger.json')

@app.route('/swagui')
@cross_origin(origin='*')
def _ui():
    return render_swaggerui(swagger_spec_path='/mystatic/swag1.json')


import io,json, ast

@app.route('/v1/swagger.json')
def _v1_spec():
    with io.open('static/swag2.json', 'r',encoding='utf8') as f: 
      data=f.read()

    if data:
       d=ast.literal_eval(data)
       return jsonify(d) #json.loads(json.dumps(d))
    else:
       return None 


@app.route('/swag1.json')
def _swag1():
    return url_for('static', filename='swag1.json')



@app.route('/v1/parsey-universal', methods=['POST'])
def _parsey_universal_handler():
    text = request.get_data()
    #print(type(text))
    if type(text) is str :
       print("str to be convert to unicode") 
       text= text.decode('utf-8')
    elif type(text) is unicode:
       print("already unicode")  
    else:
       raise ValueError(type(text)+ "not acceptable")
          
    language_code = request.headers.get('Content-Language', 'en').lower()
    print(language_code)

    try:
        conllu = parser[language_code].query(text, returnRaw=True)       
        if conllu is None:
            raise InternalServerError('Bad SyntaxNet output')
        return app.response_class(conllu, mimetype='text/plain; charset=utf-8')
    except ValueError as e:
        raise BadRequest(e)


#========= Chinese
@app.route('/v1/chinese/ud_parse', methods=['POST'])
def _chinese_ud_parse_handler():
    text = request.get_data()
    #print(type(text))
    if type(text) is str :
       print("str to be convert to unicode")
       text= text.decode('utf-8')
    elif type(text) is unicode:
       print("already unicode")
    else:
       raise ValueError(type(text)+ "not acceptable")

    language_code = 'zh'

    try:
        conllu = parser[language_code].query(text, returnRaw=True)
        if conllu is None:
            raise InternalServerError('Bad SyntaxNet output')
        return app.response_class(conllu, mimetype='text/plain; charset=utf-8')
    except ValueError as e:
        raise BadRequest(e)


app.register_blueprint(build_static_blueprint('swaggerui', __name__))

with app.test_request_context():
 list_routes()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8888)
