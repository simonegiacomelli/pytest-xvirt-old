import pytest

from xvirt.events import Evt


@pytest.hookspec()
def pytest_xvirt_setup(config):
    pass


@pytest.hookspec()
def pytest_xvirt_controlled_send_event(event: Evt):
    pass
