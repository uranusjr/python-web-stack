#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import print_function
import sys
try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:     # Python 2 compatibility
    from ConfigParser import (
        SafeConfigParser as ConfigParser, NoOptionError, NoSectionError
    )
from .utils import env


def main():
    config_path = sys.argv[1]
    set_to = sys.argv[2] if len(sys.argv) > 2 else None
    config = ConfigParser()
    config.read(env.config_file_path)

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
        except (NoSectionError, NoOptionError):
            print()
    else:                   # Set config
        if set_to:
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, option, set_to)
        else:
            try:
                config.remove_option(section, option)
            except (NoSectionError, NoOptionError):
                pass
            if not config.items(section):
                config.remove_section(section)
        with open(env.config_file_path, 'w') as f:
            config.write(f)


class ConfigArgumentError(Exception):
    pass


if __name__ == '__main__':
    main()
