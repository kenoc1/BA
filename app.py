from flask import Flask, request
import psutil
import socket

app = Flask(__name__)

hostname = "0.0.0.0"
hostport = 80
keepworking = False  # boolean to switch worker thread on or off


def _writebody(request_route):
    body = '<html><head><title>Work interface</title></head>'
    body += '<body><h2>Worker interface on ' + socket.gethostname() + '<br/>URL on ' + \
        request_route + '</h2><ul><h3>'
    body += '<br/><a href="./one">Site one</a> - <a href="./two">Site two</a> - <a href="./three">Site three</a><br/>'
    if keepworking == False:
        body += '<br/>Worker thread is not running. <a href="./do_work">Start work</a><br/>'
    else:
        body += '<br/>Worker thread is running. <a href="./stop_work">Stop work</a><br/>'
    cpu_load = psutil.cpu_percent()
    mem = psutil.virtual_memory().used
    mem_load = psutil.virtual_memory().percent
    mem_available = psutil.virtual_memory().available * 100 / \
        psutil.virtual_memory().total
    body += '<br/>Activity Monitor:<br/>CPU = ' + str(cpu_load) + '<br/>MEM = ' + str(
        mem) + '<br/>MEM (load) = ' + str(mem_load) + '<br/>MEM (available) = ' + str(mem_available) + '<br/>'
    body += '</h3></ul></body></html>'
    return body


@app.route("/")
def root():
    return _writebody(request.path)


@app.route('/one')
def one():
    return _writebody(request.path)


@app.route('/two')
def two():
    return _writebody(request.path)


@app.route('/three')
def three():
    return _writebody(request.path)


if __name__ == '__main__':
    app.run(host=hostname, port=hostport)
