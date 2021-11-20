from ipaddress import ip_address
from flask import Flask, render_template, request, Response, make_response

from users import UserHandler, IDGenerator
from utils import plot_and_show

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    user_id = IDGenerator.unique_id()
    resp = make_response(render_template("main_page.html", userID=user_id))
    return resp


@app.route("/store-txy", methods=["POST"])
def store_mouse_position():
    ip = ip_address(request.remote_addr)

    req_json = request.json
    mouse_txy_str = req_json["mouse_trajectory"]
    user_id = req_json["userID"]

    # TODO change existing-user replacement to user update
    user = UserHandler(ip_str=ip, mouse_txy_str=mouse_txy_str).user
    plot_and_show(x=user.mouse_txy.x, y=user.mouse_txy.y)
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
