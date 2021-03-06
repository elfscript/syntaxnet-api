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
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def _root():
    return redirect('/v1')


@app.route('/v1')
def _v1():
    return render_swaggerui(swagger_spec_path='/v1/swagger.json')


@app.route('/v1/parsey-universal-full', methods=['POST'])
def _parsey_universal_full_handler():
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


@app.route('/v1/swagger.json')
def _v1_spec():
    return jsonify({
        'swagger': '2.0',
        'info': {
            'version': 'dev',
            'title': 'Simple API for SyntaxNet',
            'description': 'Allows to do HTTP request to execute NLP processing using SyntaxNet',
            'license': {
                'name': 'Apache 2.0',
                'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
            }
        },
        'host': 'tensor.westus.cloudapp.azure.com:8888',
#'itek-gpu1.eastus.cloudapp.azure.com:8888',
#'tensor.westus.cloudapp.azure.com:8888',
        'basePath': '/v1',
        'paths': {
            '/parsey-universal-full': {
                'post': {
                    'summary': 'Executes the full parsing pipeline against Parsey Universal',
                    'description': 'See also https://github.com/tensorflow/models/blob/master/syntaxnet/universal.md',
                    'parameters': [
                        {
                            'name': 'text',
                            'in': 'body',
                            'description': 'The text to parse',
                            'required': True,
                            'schema': {
                                'type': 'string'
                            }
                        },
                        {
                            'name': 'Content-Language',
                            'in': 'header',
                            'description': 'The text language.',
                            'required': True,
                            'type': 'string',
                            'enum': ['en','zh']
                            # sorted(language_code_to_model_name.keys())
                        }
                    ],
                    'consumes': [
                        'text/plain; charset=utf-8'
                    ],
                    'produces': [
                        'text/plain; charset=utf-8'
                    ],
                    'responses': {
                        '200': {
                            'description': 'The parsing result in the CoNLL-U format http://universaldependencies.org/format.html'
                        },
                        '400': {
                            'description': 'Bad request, usually because the Content-Language is not supported'
                        }
                    }
                }
            }
        }
    })


app.register_blueprint(build_static_blueprint('swaggerui', __name__))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8888)
