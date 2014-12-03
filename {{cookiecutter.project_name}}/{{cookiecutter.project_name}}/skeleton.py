#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
import logging.config
import os
abspath = os.path.abspath(os.path.dirname(__file__))
os.chdir(abspath)
import re
import signal
import sys
import time

from argparse import ArgumentParser
from Queue import Queue
from threading import Lock, Thread

sys.path.append(os.path.join(abspath, "libs"))

import utils

from daemon import Daemon

# Init logging facility
logging.config.fileConfig("conf/logging.cfg")


def sigterm_handler(signum, frame):
    """Exit this application when get signal.SIGTERM signal."""
    exit()


class Tasker(object):
    def __init__(self, *args, **kwargs):
        for n, v in kwargs.iteritems():
            setattr(self, n, v)


class Config(object):

    def __init__(self, config_file):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        return

    def get_configs(self):
        self.pid_file = self.config.get("main", "pid_file")
        self.wait_time = self.config.getint("main", "wait_time")
        self.scan_task_interval = self.config.getint("main", "scan_task_interval")

        taskers = self.config.get("taskers", "keys")
        self.taskers = dict()
        for tasker in re.split(r"\s*,\s*", taskers):
            self.taskers[tasker] = self.get_tasker("tasker_{0}".format(tasker))
        return

    def get_tasker(self, tasker_name):
        tasker = Tasker(size=self.config.getint(tasker_name, "size"),
                        max_workers=self.config.getint(tasker_name, "max_workers"))
        return tasker


class Handler(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        return

    def human_readable(self, size):
        self.logger.info("{0} -> {1}".format(size, utils.approximate_size(size)))


class Skeleton(object):
    def __init__(self, config_file):
        self.logger = logging.getLogger(self.__class__.__name__)
        config = Config(config_file)
        config.get_configs()
        self.config = config
        self.lock = Lock()
        self.queues = dict()

    def produce_task(self, tasker_name, tasker):
        while True:
            try:
                queue = self.queues.get(tasker_name)
                self.logger.info("old {0} queue size: {1}".format(tasker_name, queue.qsize()))
                queue.put(tasker.size)
                self.logger.info("new {0} queue size: {1}".format(tasker_name, queue.qsize()))
            except Exception as error:
                self.logger.exception("{0} {1}".format(tasker_name, error))
            finally:
                time.sleep(self.config.scan_task_interval)
        return

    def consume_task(self, n, tasker_name, tasker):
        while True:
            handler = Handler()
            queue = self.queues.get(tasker_name)
            if queue.empty():
                time.sleep(self.config.wait_time)
                continue
            try:
                while not queue.empty():
                    size = queue.get()
                    self.lock.acquire()
                    handler.human_readable(size)
                    self.lock.release()
            except Exception as error:
                self.logger.exception('Thread-{0}: error {1}'.format(n, error))
            finally:
                del(handler)

    def do_work(self):
        for tasker_name, tasker in self.config.taskers.items():
            self.queues[tasker_name] = Queue()

            # Spwan produce_task thread
            t = Thread(target=self.produce_task, args=(tasker_name, tasker))
            t.setDaemon(True)
            t.start()

            # Spwan consume_task thread
            for n in range(tasker.max_workers):
                t = Thread(target=self.consume_task, args=(n, tasker_name, tasker))
                t.setDaemon(True)
                t.start()

        while True:
            signal.signal(signal.SIGTERM, sigterm_handler)
            # Round robin and Sleep some seconds.
            time.sleep(self.config.scan_task_interval)
        return


class SkeletonDaemon(Daemon):
    def run(self, config_file):
        skeleton = Skeleton(config_file)
        skeleton.do_work()
        return


if __name__ == "__main__":
    logger = logging.getLogger("main")
    config_file = "conf/main.cfg"
    config = Config(config_file)
    PIDFILE = config.config.get("main", "pid_file")
    daemon = SkeletonDaemon(PIDFILE)

    prog = "{{cookiecutter.package_name}}"
    parser = ArgumentParser(prog=prog, description="Daemon tool")
    parser.add_argument("action",
                        choices=("start",
                                 "stop",
                                 "restart",
                                 "status",
                                 "foreground"))
    args = parser.parse_args()
    if args.action == "start":
        logger.info("start")
        try:
            daemon.start(config)
        except Exception as error:
            logger.exception("{0} cant be started".format(prog))
    elif args.action == "stop":
        logger.info("stop")
        print("Stopping {0} ...".format(prog))
        daemon.stop()
    elif args.action == "restart":
        logger.info("restart")
        print("Restaring {0} ...".format(prog))
        daemon.restart(config)
    elif args.action == "status":
        logger.info("status")
        try:
            pf = file(PIDFILE, "r")
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None

        if pid:
            print("{0} is running as pid {1}".format(prog, pid))
        else:
            print("{0} is not running.".format(prog))
    elif args.action == "foreground":
        logger.info("foreground")
        print("Staring {0} in foreground".format(prog))
        worker = Skeleton(config_file)
        worker.do_work()
