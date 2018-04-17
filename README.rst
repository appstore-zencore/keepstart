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
        pidfile: ssh-proxy-server.pid

    keepstart:
        nic: lo
        vip: 127.0.0.1
        start: /opt/ssh-proxy-server/start.sh
        stop: /opt/ssh-proxy-server/stop.sh
        is-running: /opt/ssh-proxy-server/is-running.sh

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
