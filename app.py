from flask import Flask, render_template, request, Response, make_response

from analysis.user_base import IDGenerator
from analysis.user_handling import UserCreator, UserHandler, UserPairHandler, all_matches
from config import PREVENT_SERVER_CRASH

app = Flask(__name__)


@app.route("/", methods=["GET"])
async def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("website.html", userID=new_user_id))
    return resp


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    if PREVENT_SERVER_CRASH:
        return safe_print_and_plot()

    print_and_plot()
    return Response(status=204)


@app.route("/users-correlated-to-me", methods=["GET"])
async def correlated_users():
    return Response(status=404)


def print_and_plot() -> None:
    user = UserCreator(req=request).user()
    user_handler = UserHandler(user=user)
    user_handler.calc_and_store_metrics()
    user_handler.insert_user()
    user_handler.print_user()

    UserPairHandler().insert_valid_user_pairs()
    all_matches.print_user_pairs()

    for user_pair in all_matches:
        UserPairHandler().plot_and_save_user_pair(user_pair=user_pair)


def safe_print_and_plot() -> Response:
    try:
        print_and_plot()
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)

""" 
            HOW TO RUN IT 


Run in terminal:
    gunicorn -w 4 -b 0.0.0.0:65000 app:app

To run it normally with Tor and a normal browser you must:
    a. port-forward port 65000 in your router (or any other port you aren't using)
    b. find your IP
    c. visit <your-IP>:65000

To test it locally using only a normal browser:
    a. edit the config file to allow pair matching between non-Tor browsers
    b. Open http://0.0.0.0:65000/ on two windows (not maximized)
    c1. move mouse from one window into the other
    c2. or alt-tab and move it
    d. .. until matches are plotted.


Before re-running it, use:
    killall gunicorn


"""
