# workserver.py - simple HTTP server with a do_work / stop_work API
# GET /do_work activates a worker thread which uses CPU
# GET /stop_work signals worker thread to stop
import math
import socket
import threading
import time
import psutil
from bottle import route, run

# for STD SLB we listen on all addresses
hostname = "0.0.0.0"
#hostname = socket.gethostname()
hostport = 80
keepworking = False  # boolean to switch worker thread on or off


# thread which maximizes CPU usage while the keepWorking global is True
def workerthread():
    # outer loop to run while waiting
    while (True):
        # main loop to thrash the CPI
        while (keepworking == True):
            for x in range(1, 169):
                y = math.factorial(x)
        time.sleep(3)


# start the worker thread
worker_thread = threading.Thread(target=workerthread, args=())
worker_thread.start()


def writebody():
    body = '<html><head><title>Work interface - build</title></head>'
    body += '<body><h2>Worker interface on ' + \
        socket.gethostname() + '</h2><ul><h3>'

    if keepworking == False:
        body += '<br/>Worker thread is not running. <a href="./do_work">Start work</a><br/>'
    else:
        body += '<br/>Worker thread is running. <a href="./stop_work">Stop work</a><br/>'

    cpu_load = psutil.cpu_percent()
    mem = psutil.virtual_memory().used
    mem_load = psutil.virtual_memory().percent
    mem_available = psutil.virtual_memory().available * 100 / \
        psutil.virtual_memory().total

    body += '<br/>Activity Monitor:<br/>/CPU = ' + str(cpu_load) + '<br/>/MEM = ' + str(
        mem) + '<br/>/MEM (load) = ' + str(mem_load) + '<br/>/MEM (available) = ' + str(mem_available) + '<br/>'
    body += '<br/>Usage:<br/><br/>/do_work = start worker thread<br/>/stop_work = stop worker thread<br/>'
    body += '</h3></ul></body></html>'
    return body


@route('/')
def root():
    return writebody()


@route('/do_work')
def do_work():
    global keepworking
    # start worker thread
    keepworking = True
    return writebody()


@route('/stop_work')
def stop_work():
    global keepworking
    # stop worker thread
    keepworking = False
    return writebody()


run(host=hostname, port=hostport)
