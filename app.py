from flask import Flask, render_template, request, Response, make_response

from analysis.user_base import IDGenerator
from analysis.user_handling import UserCreator, UserHandler, UserPairHandler, all_matches, UsersPair

app = Flask(__name__)


@app.route("/", methods=["GET"])
async def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("website.html", userID=new_user_id))
    return resp


def print_metrics():
    user = UserCreator(req=request).user()
    user_handler = UserHandler(user=user)
    user_handler.calc_and_store_metrics()
    user_handler.insert_user()
    print(f"t entry {user.entry_times}")
    print(f"t exit {user.exit_times}")
    print(f"entry metrics {user.entry_metrics}")
    print(f"exit metrics {user.exit_metrics}")
    print("=" * 50)

    UserPairHandler().insert_valid_user_pairs()
    all_matches.print_user_pairs()

    for user_pair in all_matches:
        UserPairHandler().plot_user_pair(user_pair=user_pair)


def safe_print_metrics():
    try:
        print_metrics()
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response(status=204)


PREVENT_SERVER_CRASH = 0


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    if PREVENT_SERVER_CRASH:
        return safe_print_metrics()

    print_metrics()
    return Response(status=204)


@app.route("/users-correlated-to-me", methods=["GET"])
async def correlated_users():
    return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)

# Run in terminal:
#   gunicorn -w 4 -b 0.0.0.0:65000 app:app
