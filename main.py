from flask import Flask, render_template, request, Response
from data_converter import TXYConverter
from matplotlib.pyplot import plot, show

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/store-txy", methods=["POST"])
def store_mouse_position():
    ip = request.remote_addr
    mouse_txy_str = request.json["mouse_trajectory"]
    t, x, y = TXYConverter(data_string=mouse_txy_str).txy_lists()
    plot(x, y)
    show()

    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
