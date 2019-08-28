from flask import Flask
from backend import get_delivery, get_recent, partners_list, partner_info
import json
app = Flask(__name__)


@app.route("/docket/<int:number>")
def index(number):
    return json.dumps(get_delivery(number))


@app.route("/recent/<int:num>")
def recent(num):
    return json.dumps(get_recent(num))


@app.route("/partners/<string:info>")
def partners(info):
    return json.dumps(partners_list(info))


@app.route("/partners/<string:info>/<string:name>")
def info_partner(info, name):
    return json.dumps(partner_info(name, info))


if __name__ == "__main__":
    app.run()
