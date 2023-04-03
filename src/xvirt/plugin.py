# -*- coding: utf-8 -*-
import tempfile
from datetime import datetime
from pathlib import Path

import pytest


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config):
    from xvirt.vsession import VSession

    session = VSession(config)
    config.pluginmanager.register(session, "vsession")


@pytest.hookimpl
def pytest_addhooks(pluginmanager):
    from xvirt import newhooks

    pluginmanager.add_hookspecs(newhooks)


# raise Exception('got')
def pytest_addoption(parser):
    group = parser.getgroup('xvirt')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2023',
        help='Set the value for the fixture "bar".'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


def pytest_collection_modifyitems(session, config, items):
    # add the group name to nodeid as suffix if --dist=loadgroup
    pass
    config.hook.pytest_xvirt_setup(config=config)


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo


startup = datetime.now()


#
# @pytest.hookspec()
# def pytest_xvirt_setupnodes(config):
#     """called before any remote node is set up."""


@pytest.hookimpl()
def pytest_collect_file(file_path: Path, path, parent):
    tmpdir = Path(tempfile.tempdir) / 'collect_file'
    tmpdir.mkdir(exist_ok=True)
    collect_dir = tmpdir / (f'cf_' + startup.strftime("%Y-%m-%d_%H-%M-%S_%f") + '.txt')
    # assert str(collect_dir) is None
    if file_path.name == 'some_test.py':
        print('pass')
    with collect_dir.open('a') as f:
        f.write(str(file_path) + f' parent={parent}\n')


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    # do_something_before_next_hook_executes()

    outcome = yield
    # outcome.excinfo may be None or a (cls, val, tb) tuple

    res = outcome.get_result()  # will raise if outcome was exception

    # post_process_result(res)

    # outcome.force_result(new_res)
