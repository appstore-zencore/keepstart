keepstart
=========

Monitor keepalived status, run start.sh if server get MASTER role, and run stop.sh if server get SLAVE role.

Install
-------

::

    pip install keepstart


Example Config
--------------

::

    application:
        daemon: true
        workspace: /opt/ssh-proxy-server
        pidfile: ssh-proxy-server.pid

    keepstart:
        nic: lo
        vip: 127.0.0.1
        start: /opt/ssh-proxy-server/start.sh
        stop: /opt/ssh-proxy-server/stop.sh
        is-running: /opt/ssh-proxy-server/is-running.sh
        sleep: 2
        running-report-cycle: 3600
        force-test-cycle: 60

    logging:
        version: 1
        disable_existing_loggers: false
        formatters:
            simple:
                format: "%(asctime)-15s\t%(levelname)s\t%(message)s"
        handlers:
            console:
                class: logging.StreamHandler
                level: DEBUG
                formatter: simple
            file:
                class: logging.handlers.TimedRotatingFileHandler
                level: DEBUG
                formatter: simple
                filename: /opt/ssh-proxy-server/server.log
                backupCount: 30
                when: D
                interval: 1
                encoding: utf-8
        loggers:
            keepstart:
                level: INFO
                handlers:
                    - file
                    - console
                propagate: no
        root:
            level: INFO
            handlers:
                - file
                - console

Config to use separated logging.conf
------------------------------------


1. config.yaml

::

    application:
        daemon: true
        workspace: /opt/ssh-proxy-server
        pidfile: ssh-proxy-server.pid

    keepstart:
        nic: lo
        vip: 127.0.0.1
        start: /opt/ssh-proxy-server/start.sh
        stop: /opt/ssh-proxy-server/stop.sh
        is-running: /opt/ssh-proxy-server/is-running.sh
        sleep: 2
        running-report-cycle: 3600
        force-test-cycle: 60

    logging: logging.conf

set logging to the config file in config.yaml, and create logging.conf file.

2. logging.conf

::

    [loggers]
    keys=root,keepserver,appserver

    [handlers]
    keys=consoleHandler,fileHandler

    [formatters]
    keys=simpleFormatter

    [logger_root]
    level=DEBUG
    handlers=consoleHandler,fileHandler

    [logger_keepserver]
    level=DEBUG
    handlers=consoleHandler,fileHandler
    qualname=keepserver
    propagate=0

    [logger_appserver]
    level=DEBUG
    handlers=consoleHandler,fileHandler
    qualname=appserver
    propagate=0

    [handler_consoleHandler]
    class=StreamHandler
    level=DEBUG
    formatter=simpleFormatter
    args=(sys.stdout,)

    [handler_fileHandler]
    class=logging.handlers.TimedRotatingFileHandler
    level=DEBUG
    formatter=simpleFormatter
    args=('logFile.log', 'D', 1, 30, 'utf-8')

    [formatter_simpleFormatter]
    format=%(asctime)s %(levelname)5s %(message)s

You must add logger_xxx which xxx is the module to be actived for logging.

Config item description
-----------------------

1. keepstart.nic

    Which nic to be monitored.

1. keepstart.vip

    Which vip will be used on the given nic. If vip is set, the server got MASTER role, if vip is not set, the server got SLAVE role.

1. keepstart.start & keepstart.stop & keepstart.is-running

    Scripts to do start, stop and is-running test. All scripts must NOT blocked.

1. keepstart.sleep

    How long time to wait to do role test.

1. keepstart.running-report-cycle

    How long time to wait to write alive report to log.

1. keepstart.force-test-cycle

    How many time to wait to do a force is-running check(time = sleep * force-test-cycle).

Server command
--------------

::

    keepserver -c config.yaml start
    keepserver -c config.yaml stop
    keepserver -c config.yaml reload

Command help
------------

::

    zencoreDeMacPro:keepstart zencore$ keepserver --help
    Usage: keepserver [OPTIONS] COMMAND [ARGS]...

    Options:
    -c, --config FILENAME  Config file path, use yaml format. Default to
                            config.yaml.
    --help                 Show this message and exit.

    Commands:
    reload  Reload application server.
    start   Start application server.
    stop    Stop application server.
    zencoreDeMacPro:keepstart zencore$
