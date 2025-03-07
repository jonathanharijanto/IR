import logging
import logging.handlers
import os
import sys
import argparse
import uuid

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from datamodel.search.QiushibaiAvinashkumarKyungwoohyunJonathanharijanto_datamodel import QiushibaiAvinashkumarKyungwoohyunJonathanharijantoProjectionLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Deleter, Getter
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4
from spacetime.client.frame import frame

logger = logging.getLogger(__name__)
LOG_HEADER = "[DELETEFRONTIER]"

@Deleter(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoProjectionLink)
@Getter(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoProjectionLink)
class DeleteFrontierFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "QiushibaiAvinashkumarKyungwoohyunJonathanharijanto"
        self.frame = frame


    def initialize(self):
        pass

    def update(self):
        print "Deleting links. This might take a while."
        ls = self.frame.get(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoProjectionLink)
        print "Found ", len(ls), " links to delete."
        for l in ls:
            self.frame.delete(QiushibaiAvinashkumarKyungwoohyunJonathanharijantoProjectionLink, l)
        print "Deleted all links."
        self.done = True

    def shutdown(self):
        pass

logger = None

class Simulation(object):
    '''
    classdocs
    '''
    def __init__(self, address, port):
        '''
        Constructor
        '''
        frame_c = frame(address = "http://" + address + ":" + str(port) + "/", time_step = 1000)
        frame_c.attach_app(DeleteFrontierFrame(frame_c))

        frame_c.run_async()
        frame.loop()

def SetupLoggers():
    global logger
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)

    #logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
    #flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
    #flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
    #logger.addHandler(flog)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CRAWLER'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, default="amazon.ics.uci.edu", help='Address of the distributing server')
    parser.add_argument('-p', '--port', type=int, default=9300, help='Port used by the distributing server')
    args = parser.parse_args()
    SetupLoggers()
    sim = Simulation(args.address, args.port)