from ipaddress import ip_address

from flask import Flask, render_template, request, Response
from data_converter import TXYConverter

from users import update_user, User, TimeXY, TimeKeys
from utils import plot_and_show

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/store-txy", methods=["POST"])
def store_mouse_position():
    ip = ip_address(request.remote_addr)
    mouse_txy_str = request.json["mouse_trajectory"]
    t, x, y = TXYConverter(data_string=mouse_txy_str).txy_lists()

    user = User(ip=ip,
                mouse_txy=TimeXY(time=t, x=x, y=y),
                time_keys=TimeKeys(keys_pressed=[], time=[]))
    update_user(user=user)

    plot_and_show(x, y)

    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
