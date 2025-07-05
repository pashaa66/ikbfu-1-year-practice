from flask import Flask, render_template
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.basedir,
                                           "static", "img", "uploads")


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register_menu.html", title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)
