from flask import Flask, render_template, request, Response, make_response, jsonify

from users import UserHandler, IDGenerator

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("main_page.html", userID=new_user_id))
    return resp


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    user_handler = UserHandler(req=request)
    user_handler.create_user()
    user_handler.plot_mouse_movement()
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
