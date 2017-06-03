import flask
from flask import Flask, url_for
app = Flask(__name__, static_url_path='/mystatic2')
print("flask.__version__", flask.__version__)
print("app.static_url_path",  app.static_url_path)
print("app.static_folder", app.static_folder)
print("app.root_path", app.root_path)
print("app.instance_path", app.instance_path)
print("app.config", app.config)


@app.route('/')
def hello_world():
    return 'Hello, Flask Dockerized'

@app.route('/test1')
def test1():  
    return url_for('static', filename='test1.txt')

@app.route('/s1/<path:path>')
def s1():
    return send_from_directory('mystatic', path)



if __name__ == '__main__':
      app.run(debug=True,host='0.0.0.0', port=8888)
