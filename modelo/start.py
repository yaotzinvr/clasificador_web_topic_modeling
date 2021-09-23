import flask, os
from flask_cors import CORS
import topic_modeling

app = flask.Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def home():
    return 'Modelo ML del proyecto Clasificador Web Topic Modeling'

@app.route('/topic-modeling/get', methods=['POST'])
def topic_modeling_get():
    args = {}
    for x in ['texto_completo',]:
        args[x] = flask.request.get_json()[x] if flask.request.get_json() else flask.request.args[x]
    r = topic_modeling.get(**args)
    if not r['ok']: return flask.jsonify(r), r['code']
    return r['data']

if __name__=='__main__':
    app.run(host=(os.environ['MODEL_HOST'] if 'MODEL_HOST' in os.environ else '0.0.0.0'),
            port=(os.environ['MODEL_PORT'] if 'MODEL_PORT' in os.environ else 8080),
            debug=False,
            )
