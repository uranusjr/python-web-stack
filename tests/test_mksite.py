#!/usr/bin/env python
# -*- coding: utf-8

import os.path
import pwd
from nose.tools import ok_, eq_, with_setup
from pywebstack import mksite, utils
from . import *


utils.env.update({
    'virtualenv_root': os.path.join(TEMP_DIR, 'virtualenv'),
    'nginx_conf_dir': os.path.join(TEMP_DIR, 'nginx', 'available'),
    'nginx_conf_link_dir': os.path.join(TEMP_DIR, 'nginx', 'enabled'),
    'startup_script_dir': os.path.join(TEMP_DIR, 'init.d')
})


def _create_tempdirs():
    create_tempdir()
    utils.mkdir_p(utils.env.virtualenv_root)
    utils.mkdir_p(utils.env.nginx_conf_dir)
    utils.mkdir_p(utils.env.nginx_conf_link_dir)
    utils.mkdir_p(utils.env.startup_script_dir)


def _setup_permission_test():
    test_dir = os.path.join(TEMP_DIR, 'permission_fix_test_dir')
    test_file = os.path.join(test_dir, 'test')
    os.makedirs(test_dir)
    with open(test_file, 'w+'):
        pass
    os.chown(test_dir, 0, -1)
    os.chown(test_file, 0, -1)


@with_setup(setup=_create_tempdirs, teardown=cleanup_tempdir)
def test_make_virtualenv():
    cl_args = MockedArguments(name=PROJECT_NAME)
    mksite.make_virtualenv(cl_args)

    virtualenv_path = utils.normalize(utils.env.virtualenv_root, PROJECT_NAME)
    ok_(os.path.exists(virtualenv_path))
    ok_(os.path.exists(
        utils.normalize(virtualenv_path, utils.env.project_container_name)
    ))


# This test does not actually work because we can't change ownership for
# things in tempdir. Need to find another way to implement this test.
@skipped
@with_setup(setup=_setup_permission_test, teardown=cleanup_tempdir)
def test_fix_permission():
    test_dir = os.path.join(TEMP_DIR, 'permission_fix_test_dir')
    test_file = os.path.join(test_dir, 'test')
    mksite.fix_permission(test_dir)

    get_owner_name = lambda p: pwd.getpwuid(os.stat(p).st_uid).pw_name
    eq_(get_owner_name(test_dir), os.getlogin())
    eq_(get_owner_name(test_file), os.getlogin())


@with_setup(setup=_create_tempdirs, teardown=cleanup_tempdir)
def test_add_nginx_conf():
    filename = 'test_file'
    content = (
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim '
        'ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '
        'aliquip ex ea commodo consequat. Duis aute irure dolor in '
        'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
        'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
        'culpa qui officia deserunt mollit anim id est laborum.'
    )
    mksite.add_nginx_conf(filename, content)

    conf_path = os.path.join(utils.env.nginx_conf_dir, filename)
    link_path = os.path.join(utils.env.nginx_conf_link_dir, filename)
    ok_(os.path.isfile(conf_path))
    ok_(os.path.islink(link_path))
    eq_(os.path.realpath(link_path), os.path.realpath(conf_path))

    with open(conf_path, 'r') as f:
        eq_(f.read(), content)


@with_setup(setup=_create_tempdirs, teardown=cleanup_tempdir)
def test_add_startup_conf():
    filename = 'test_file'
    content = (
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim '
        'ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '
        'aliquip ex ea commodo consequat. Duis aute irure dolor in '
        'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
        'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
        'culpa qui officia deserunt mollit anim id est laborum.'
    )
    mksite.add_startup_conf(filename, content)
    with open(os.path.join(utils.env.startup_script_dir, filename), 'r') as f:
        eq_(f.read(), content)


if __name__ == '__main__':
    import nose
    nose.run(argv=[__file__, '--with-doctest', '-vv'])
