#!/usr/bin/python
print("Content-type: text/html \n")

"""Using CGI instead of flask."""

import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()
lang = form.getvalue("lang")
prog = form.getvalue("prog")

import subprocess, re, os

data = {
    "lang": lang,
    "prog": prog,
}

def process_java(prog):
    match = re.match(r"public class (?P<classname>\w+)", prog)
    cwd = os.getcwd() + "/cgi-bin/"
    classname = cwd + match["classname"]
    filename = classname + ".java"
    with open(filename, mode="w") as f:
        f.write(prog)
        os.chmod(filename, 0o744)
    output = subprocess.run(f"javac -d {filename}", shell=True, capture_output=True)
    os.chmod(f"{classname}.class", 0o744)
    output = subprocess.run(f"java -cp {cwd} {match['classname']}", shell=True, capture_output=True)

    print(output.stdout.decode("utf-8"))



process_lang = {
    "java": process_java(data["prog"]),
}


process_lang[data["lang"]]

