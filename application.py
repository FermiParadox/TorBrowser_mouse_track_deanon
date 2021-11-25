from flask import Flask, render_template, request, Response, make_response

from users import UserHandler, IDGenerator

app = Flask(__name__)


@app.route("/", methods=["GET"])
async def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("main_page.html", userID=new_user_id))
    return resp


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    try:
        user_handler = UserHandler(req=request)
        user_handler.create_user()
        user_handler.user.plot_and_show_mouse_movement()
        print(f"t {user_handler.user.time_keys}")
        print(f"t {user_handler.user.time_keys}")
        print(f"ang {user_handler.user.exit_angles()}")
        print(f"ang {user_handler.user.entry_angles()}")
        print(f"sp {user_handler.user.exit_speeds()}")
        print(f"sp {user_handler.user.entry_speeds()}")
        print(f"acc {user_handler.user.exit_accelerations()}")
        print(f"acc {user_handler.user.entry_accelerations()}")
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response(status=204)


@app.route("/users-correlated-to-me", methods=["GET"])
async def correlated_users():
    return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)
