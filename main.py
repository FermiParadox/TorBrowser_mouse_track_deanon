from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/store-txy", methods=["POST"])
def store_mouse_position():
    ip = request.remote_addr
    txy_data = request.json["mouse_trajectory"]
    return ''





if __name__ == "__main__":
    app.run(debug=True)
