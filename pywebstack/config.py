#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import print_function
try:
    from configparser import ConfigParser
except ImportError:     # Python 2 compatibility
    from ConfigParser import SafeConfigParser as ConfigParser
from .utils import normalize


def main(config_path, set_to=None):
    config_file_path = normalize('config.cfg')
    config = ConfigParser()
    try:
        with open(config_file_path) as f:
            config.readfp(f)
    except IOError:     # File does not exist
        config.add_section('path')

    try:
        section, option = config_path.split('.')
    except ValueError:  # Cannot expand the path to exactly two items
        raise ConfigArgumentError(
            'Config name needs to consist a two-part string, seperated by a '
            'dot (.).'
        )

    if set_to is None:      # Get config
        try:
            print(config.get(section, option))
        except ConfigParser.NoOptionError:
            print()
    else:
        if set_to:
            config.set(section, option, set_to)
        else:
            config.remove_option(section, option)
        with open(config_file_path, 'w') as f:
            config.write(f)


class ConfigArgumentError(Exception):
    pass


if __name__ == '__main__':
    main('')