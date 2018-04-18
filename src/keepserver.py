from __future__ import print_function
import os
import logging
from logging import config as logging_config
import signal
import time
import threading
import psutil
from appserver import server as main_server
from appserver import set_config_loader
from appserver import default_config_loader
from dictop import select
from dictop import update


logger = logging.getLogger(__name__)
stop_flag = threading.Event()


def findvip(vip, nic=None):
    nics = psutil.net_if_addrs()
    if nic:
        if not nic in nics:
            logger.error("Nic {name} not found in current system.".format(name=nic))
            return None
        addrs = nics[nic]
        for addr in addrs:
            if addr.address == vip:
                return True
    else:
        for addrs in nics.values():
            for addr in addrs:
                if addr.address == vip:
                    return True
    return False


def call(command):
    exit_code = -1
    try:
        exit_code = os.system(command)
    finally:
        if exit_code == 0:
            logger.info("Call command: {command} SUCCESS.".format(command=command))
        else:
            logger.warn("Call command: {command} FAILED with exit_code = {exit_code}.".format(command=command, exit_code=exit_code))
    return exit_code == 0


def is_running(command, current_status, counter, force_test_cycle, force):
    # command is None, trust current_status
    if command is None:
        if current_status is None:
            return False
        else:
            return current_status
    # do force check
    # only if not force, we may trust current_status
    # only if current_status is not None, we many trust current_status
    if (not force) and (current_status is not None):
        if counter % force_test_cycle:
            return current_status
    logger.info("Test is running with command: {command}".format(command=command))
    # do test
    try:
        exit_code = os.system(command)
        if exit_code == 0:
            return True
        else:
            return False
    except:
        return None


def server(config):
    # setup logging
    logging_config_data = select(config, "logging")
    if not logging_config_data:
        logging.basicConfig()
    elif logging_config_data and isinstance(logging_config_data, dict) and hasattr(logging_config, "dictConfig"):
        logging_config.dictConfig(logging_config_data)
    elif logging_config_data and isinstance(logging_config_data, str):
        logging_config.fileConfig(logging_config_data)
    # clean stop_flag
    stop_flag.clear()
    # get config item value
    sleep = select(config, "keepstart.sleep", 2)
    vip = select(config, "keepstart.vip")
    start = select(config, "keepstart.start")
    stop = select(config, "keepstart.stop")
    nic = select(config, "keepstart.nic")
    report = select(config, "keepstart.running-report-cycle", 60*60)
    force_test_cycle = select(config, "keepstart.force-test-cycle", 60)
    is_running_test_command = select(config, "keepstart.is-running")
    force_test_flag = False
    is_running_flag = None
    counter = 0
    # catch signal and stop server
    def on_exit(sig, frame):
        stop_flag.set()
        msg = "Server got signal {sig}, set stop_flag=True and exiting...".format(sig=sig)
        print(msg, file=os.sys.stderr)
        logger.info(msg)
    try:
        signal.signal(signal.SIGINT, on_exit)
        signal.signal(signal.SIGTERM, on_exit)
    except:
        logger.exception("Install signal failed, but program will keep on running...")
    # do main loop
    while not stop_flag.is_set():
        try:
            time.sleep(sleep)
            counter += 1
            if counter % report:
                logger.debug("Keep-server is running with counter={counter}.".format(counter=counter))
            is_master = findvip(vip, nic)
            if is_master is None:
                logger.error("Find vip failed vip={vip} nic={nic}.".format(vip=vip, nic=nic))
                continue
            is_running_flag = is_running(is_running_test_command, is_running_flag, counter, force_test_cycle, force_test_flag)
            if is_running_flag is None:
                logger.error("Test main program running status failed, test command: {command}.".format(command=is_running_test_command))
                continue
            if is_master and not is_running_flag:
                is_running_flag = True
                logger.info("System got MASTER role, but main program is NOT running, start it!")
                call(start)
                force_test_flag = True
                continue
            if is_running_flag and not is_master:
                is_running_flag = False
                logger.info("System got BACKUP role, and main program is RUNNING, stop it!")
                call(stop)
                force_test_flag = True
                continue
            force_test_flag = False
        except:
            logger.exception("Server main-loop got error.")
    # finished main loop
    logger.info("Server finished.")

def config_loader(config):
    data = default_config_loader(config)
    update(data, "application.main", "keepserver.server")
    return data

def main():
    set_config_loader(config_loader)
    main_server()

if __name__ == "__main__":
    main()
