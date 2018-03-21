#!/usr/bin/env python
from appserver import server
from appserver import set_config_loader
from appserver import default_config_loader
from dictop import update


def config_loader(config):
    data = default_config_loader(config)
    update(data, "application.main", "keepstart.server")
    return data

if __name__ == "__main__":
    set_config_loader(config_loader)
    server()
