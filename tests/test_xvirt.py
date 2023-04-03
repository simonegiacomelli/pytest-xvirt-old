# -*- coding: utf-8 -*-
import json
from pathlib import Path
from queue import Queue

from pytest import Pytester

from xvirt.events import EvtCollectionFinish
from xvirt.remote import RemoteEndpoint

_queue = Queue()


def remote_transport_send(payload: bytes) -> None:
    _queue.put(payload)


def test_module_full_name():
    """just a reminder that __name__ has the full package path :)"""
    assert __name__ == 'tests.' + Path(__file__).stem
    assert remote_transport_send.__name__ == ''


def test_send_events(pytester: Pytester):
    # Controlled()
    target = EvtCollectionFinish(['ciao1', 'ciao2'])
    string = json.dumps((target, target))
    assert string == ''

    remote_transport = __name__ + '.' + remote_transport_send.__name__

    # pytester.runpytest_inprocess(f'--xvirt-remote-transport={remote_transport}')


def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_sth(bar):
            assert bar == "europython2015"
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '--foo=europython2015',
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'xvirt:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])


def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
