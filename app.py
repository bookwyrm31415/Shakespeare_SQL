from flask import Flask, render_template, request
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("static\shakespeare.db")
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method != "POST":
        return render_template("index.html")
    else:
        conn = get_db_connection()

        lines = conn.execute(
            f"select * from playsearch join shakespeare on playsearch.playsrowid = shakespeare.dataline where text match '{request.form['searchLine']}'"
        ).fetchall()

        print(len(lines))
        print(request.form["searchLine"])
        conn.close()
        return render_template("index.html", lines=lines)


@app.route("/about")
def about():
    return render_template("about.html")
