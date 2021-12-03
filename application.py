from flask import Flask, render_template, request, Response, make_response

from users import UserHandler, IDGenerator, all_users

app = Flask(__name__)


@app.route("/", methods=["GET"])
async def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("website.html", userID=new_user_id))
    return resp


def print_metrics():
    user_handler = UserHandler(req=request)
    user_handler.create_and_insert_user()
    user = user_handler.user
    user.plot_and_show_mouse_movement()
    print(f"t exit {user.mouse_exit_times}")
    print(f"t entry {user.mouse_entry_times}")
    print(f"angles exit {user.exit_angles()}")
    print(f"angles entry {user.entry_angles()}")
    # print(f"speed exit {user.exit_speeds()}")
    # print(f"speed entry {user.entry_speeds()}")
    # print(f"a exit {user.exit_accelerations()}")
    # print(f"a entry {user.entry_accelerations()}")
    print("=" * 50)


def try_print_metrics():
    try:
        print_metrics()
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response(status=204)


PREVENT_SERVER_CRASH = 1


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    if PREVENT_SERVER_CRASH:
        return try_print_metrics()

    print_metrics()
    return Response(status=204)


@app.route("/users-correlated-to-me", methods=["GET"])
async def correlated_users():
    return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)

# Run in terminal:
#   gunicorn -w 4 -b 0.0.0.0:65000 application:app
