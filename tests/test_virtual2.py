from pytest import Pytester


def test_plugin_run_remotely(pytester: Pytester):
    pytester.makeconftest("""
import pytest
@pytest.hookimpl
def pytest_xvirt_setup(config):
    #1/0
    pass

    """)
    remote = pytester.mkpydir('remote')
    (remote / 'some_test.py').write_text(
        """
def test_1():
    pass
    # from js import document
    """
    )

    pytester.runpytest().assert_outcomes(passed=1)
