from ipaddress import ip_address

from flask import Flask, render_template, request, Response

from users import UserCreator
from utils import plot_and_show

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/store-txy", methods=["POST"])
def store_mouse_position():
    ip = ip_address(request.remote_addr)
    mouse_txy_str = request.json["mouse_trajectory"]

    user = UserCreator(ip_str=ip, mouse_txy_str=mouse_txy_str).user
    plot_and_show(x=user.mouse_txy.x, y=user.mouse_txy.y)
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
