"""Proof-of-concept testing without the Flask overhead."""

import subprocess, re, os
import sys

prog = """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, compiler!");
    }
}
"""

prog = sys.argv[1]

lang = "java"

data = {
    "lang": lang,
    "prog": prog,
}

def process_java(prog):
    match = re.match(r"public class (?P<classname>\w+)", prog)
    classname = match["classname"]
    filename = classname + ".java"
    with open(filename, mode="w") as f:
        f.write(prog)
    output = \
        subprocess.check_output(
            f"javac {filename} && java {classname}", shell=True
        )
    print(output)
    os.remove(classname + ".class")
    os.remove(filename)
    


process_lang = {
    "java": process_java(data["prog"]),
}


process_lang[data["lang"]]
