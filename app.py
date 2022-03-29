from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

import subprocess, re, os

app.config["SECRET_KEY"] = "IFJFJ)#J@#F(F)#FJFO#@WJF"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compiler", methods=["GET", "POST"])
def compiler():
    if request.method == "POST":
        lang = request.form["lang"]
        session["prog"] = request.form["prog"]
        return redirect(url_for(lang))
    return render_template("compiler.html")


@app.route("/java")
def java():
    prog = session.get("prog")
    match = re.match(r"public class (?P<classname>\w+)", prog)
    classname = match["classname"]
    filename = classname + ".java"
    with open(filename, mode="w") as f:
        f.write(prog)
    output = subprocess.check_output(
        f"javac {filename} && java {classname}", shell=True
    ).decode("utf-8")
    session["output"] = output
    os.remove(classname + ".class")
    os.remove(filename)
    return redirect(url_for("output"))


@app.route("/output")
def output():
    return render_template("output.html", output=session.get("output"))
