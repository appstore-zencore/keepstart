import os
import logging
import psutil
import time
from dictop import select


logger = logging.getLogger(__name__)


def findvip(vip, nic=None):
    nics = psutil.net_if_addrs()
    if nic:
        if not nic in nics:
            logger.error("Nic {} not found in current system.".format(nic))
            return False
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
            logger.info("Call command: {} SUCCESS.".format(command))
        else:
            logger.warn("Call command: {} FAILED with exit_code = {}.".format(command, exit_code))
    return exit_code == 0


def guard(is_running, vip, start, stop, nic=None):
    is_master = findvip(vip, nic)
    is_running = callable(is_running) and is_running() or is_running
    if is_master and not is_running:
        logger.info("System got MASTER role, and main program is NOT running, start it!")
        call(start)
        return True
    if is_running and not is_master:
        logger.info("System got BACKUP role, and main program is RUNNING, stop it!")
        call(stop)
        return False
    return is_running


def server(config):
    vip = select(config, "keepstart.vip")
    start = select(config, "keepstart.start")
    stop = select(config, "keepstart.stop")
    nic = select(config, "keepstart.nic")
    sleep = select(config, "keepstart.sleep", 2)
    is_running = False
    while True:
        is_running = guard(is_running, vip, start, stop, nic)
        time.sleep(sleep)
