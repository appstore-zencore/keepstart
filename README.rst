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
        daemon: false
        workspace: /opt/app
        pidfile: jenkins-keep.pid
    keepstart:
        nic: eth0
        vip: 172.18.1.44
        start: /opt/app/start.sh
        stop: /opt/app/stop.sh
        is-running: /opt/app/status.sh
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
        loggers:
            keepstart:
                level: DEBUG
                handlers:
                    - console
                propagate: no
        root:
            level: DEBUG
            handlers:
                - console

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
