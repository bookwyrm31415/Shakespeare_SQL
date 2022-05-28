from flask import Flask, render_template, request
from werkzeug.exceptions import abort
import sqlite3
import string


def get_db_connection():
    conn = sqlite3.connect("static\shakespeare.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_scene(play, act, scene):
    conn = get_db_connection()
    lines = conn.execute(
        "SELECT * FROM shakespeare WHERE play = ? and act = ? and scene = ? order by dataline",
        (play, act, scene),
    ).fetchall()
    conn.close()
    if lines is None:
        abort(404)
    return lines


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method != "POST":
        return render_template("index.html")
    else:
        conn = get_db_connection()
        searchline = request.form["searchLine"]
        # Removes punctuation
        searchline = searchline.translate(str.maketrans("", "", string.punctuation))

        lines = conn.execute(
            f"select * from playsearch join shakespeare on playsearch.playsrowid = shakespeare.dataline where text match ?",
            (searchline,),
        ).fetchall()

        print(len(lines))
        print(request.form["searchLine"])
        conn.close()
        return render_template("index.html", lines=lines, length = len(lines))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/scene")
def scene():
    play = request.args.get("play", "")
    act = request.args.get("act", "")
    scene = request.args.get("scene", "")

    lines = get_scene(play, act, scene)

    return render_template("scene.html", lines=lines)
