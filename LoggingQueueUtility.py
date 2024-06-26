import logging
import logging.handlers
import multiprocessing
import LoggingUtility

# Listener configuration
def listener_configurer():
    queuelogger = logging.getLogger("files")
    # root = logging.getLogger()
    # h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
    # f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    # h.setFormatter(f)
    # root.addHandler(h)

# Listener process
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:
                # Sentinel to quit the listener
                break
            queuelogger = logging.getLogger("files")
            queuelogger.handle(record)  # No level or filter logic applied
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

log_queue = multiprocessing.Queue(-1)
listener = multiprocessing.Process(target=listener_process, args=(log_queue, listener_configurer))
listener.start()

# Create log and set handler to queue handle
logger = logging.getLogger("queue")
# logger.setLevel(logging.DEBUG)  # Log level = DEBUG
qh = logging.handlers.QueueHandler(log_queue)
qh.setLevel(logging.DEBUG)
logger.addHandler(qh)
logger.info('Look out!')  # Create INFO message
logger.error("heres and error!")

log_queue.put(None)  # Signal listener to quit
listener.join()
