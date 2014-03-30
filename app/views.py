from app import app
from flask import render_template, request, jsonify, session, Markup
#from pypysandbox import exec_sandbox # use pypy sanbox for execution
from pyscriptrunner import runprocess
from Queue import Queue, Empty

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/repl', methods=['GET'])
@app.route('/repl/', methods=['GET'])
def execute():
    code = request.args.get("code")
    # process stdout for beautiful print
    statement = code.replace('\r\n', '\n')
    statement += '\n\n'

    result = runprocess(statement)

    out = err = ''
    while True:
        try:
            std = result.get(True, 1)
            if std[0] == 'STDOUT':
                out += std[1]
            else:
                err += std[1]
        except Empty:
            break
    #print out

    return jsonify(success=1, output=out, error=err)

