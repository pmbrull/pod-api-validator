import flask
import requests
from pyshex import ShExEvaluator

from utils import BearerAuth, MyPrefixLibrary


_pod = "https://pmbrull.solid.community"
_auth_token = "<pod-token>"

_shex = """
PREFIX ex: <#>
PREFIX n0: <http://shapes.pub/shapes/activity.shex#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

ex:HKData {
  n0:calories      xsd:string;
  n0:date          xsd:string;
  n0:distance      xsd:string;
  n0:score         xsd:string;
  n0:steps         xsd:string
}
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h2> querying pod API </h2>"

@app.route('/get-data', methods=['GET'])
def get_data():
    r = requests.get(
        _pod + "/my-files/20200206.ttl",
        auth=BearerAuth(_auth_token)
    )
    return r.text

@app.route('/get-data-validate', methods=['GET'])
def get_data_validate():
    rdf = get_data()

    p = MyPrefixLibrary()
    p.add_rdf(rdf)
    p.add_shex(_shex)

    results = ShExEvaluator(rdf=rdf,
                            schema=_shex,
                            focus=[p.get_namespace('').data],
                            start=p.EX.HKData).evaluate()

    if (all(res.result for res in results)):
        print("Validation passed!")
        return rdf
    else:
        print("Something went wrong!")
        return "<h1> VALIDATION ERROR </h1>"

app.run()
