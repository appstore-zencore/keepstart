keepstart
=========

Monitor keepalived status, run start.sh if server get MASTER role, and run stop.sh if server get SLAVE role.

Install
-------

    pip install keepstart


Example Config
--------------

    application:
        daemon: false
        pidfile: jenkins-keep.pid

    keepstart:
        nic: eth0
        vip: 172.18.1.44
        start: /opt/app/start.sh
        stop: /opt/app/stop.sh
        is-running: /opt/app/status.sh

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

