import time
from random import randrange

from flask import Flask, render_template, request
from pyecharts.charts import Bar

from statistics import Models

app = Flask(__name__, static_folder="templates")


def bar_base(modelId) -> Bar:
    models = Models.select().where(Models.id == modelId).order_by(Models.timestamp).execute()
    xaxis = list()
    yaxis = list()
    for model in models:
        y_title = model.name
        yaxis.append(model.runCount + model.downloadCount)
        xaxis.append(model.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    c = (
        Bar()
        .add_xaxis(xaxis)
        .add_yaxis(y_title, yaxis)
    )
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart")
def get_bar_chart():
    modelId = request.args.get('modelId')
    c = bar_base(modelId)
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()
